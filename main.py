import os
import logging
import time

import requests

from dotenv import load_dotenv
from terminaltables import AsciiTable


HH_URL = 'https://api.hh.ru/vacancies'
SP_URL = 'https://api.superjob.ru/2.0/vacancies'
PERIOD_PLACEMENT = 30

POPULAR_PROGRAMMING_LANGUAGES = [
        'Go',
        'C',
        'C#',
        'C++',
        'PHP',
        'Ruby',
        'Python',
        'Java',
        'JavaScript'
    ]


def get_hh_salary_statistics(vacancy: str, url: str, period_placement: int) -> dict:
    city_id = 1
    payload = {
            'text': vacancy,
            'area': city_id,
            'period': period_placement,
            'only_with_salary': True,
            'per_page': 100,
            'page': 0
        }

    average_salary = 0
    vacancies_processed = 0

    while True:
        response = requests.get(url, params=payload)
        response.raise_for_status()

        response_content = response.json()

        vacancies = response_content['items']
    
        for vacancy in vacancies:
            salary_vacancy = vacancy['salary']
            payment_from = salary_vacancy['from']
            payment_to = salary_vacancy['to']

            currency_flag = salary_vacancy['currency'] == 'RUR'
            salary = predict_rub_salary(payment_from, payment_to)

            if currency_flag and salary:
                average_salary += salary
                vacancies_processed += 1

        payload['page'] += 1

        pages_flag = payload['page'] == response_content['pages']

        if pages_flag:
            vacancies_found = response_content['found']

            break
    
    average_salary = int(average_salary / vacancies_processed)

    language_statistics = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary,
        }

    return language_statistics


def get_sj_salary_statistics(vacancy: str, url: str, token: str, period_placement: int) -> dict:
    payload = {
        'town': 'Москва',
        'keyword': vacancy,
        'period': period_placement,
        'currency': 'rub',
        'count': 100
    }
    headers = {
        'X-Api-App-Id': token,
    }

    response = requests.get(url, params=payload, headers=headers)
    response.raise_for_status()

    response = response.json()

    vacancies = response['objects']

    average_salary = 0
    vacancies_processed = 0

    vacancies_found = response['total']

    for vacancy in vacancies:
        payment_from = vacancy['payment_from']
        payment_to = vacancy['payment_to']

        salary = predict_rub_salary(payment_from, payment_to)

        if salary:
            average_salary += salary
            vacancies_processed += 1

    average_salary = int(average_salary / vacancies_processed)

    language_statistics = {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary,
    }

    return language_statistics


def predict_rub_salary(payment_from, payment_to) -> None|int:
    if payment_from and payment_to:
        average_salary = int((payment_from + payment_to)/2)

        return average_salary

    if payment_from and not payment_to:
        average_salary = int(payment_from * 1.2)

        return average_salary

    if not payment_from and payment_to:
        average_salary = int(payment_to * 0.8)

        return average_salary


def make_table(salary_statistics, title):
    column_names = [
        ['Язык программирования', 'Вакансий найдено',
        'Вакансий обработано', 'Средняя зарплата']
    ]
    for language, statistics in salary_statistics.items():
        column_content = [
            language, statistics['vacancies_found'],
            statistics['vacancies_processed'], statistics['average_salary']
        ]
        column_names.append(column_content)
    
    table_instance = AsciiTable(column_names, title)

    return table_instance.table


def main():
    load_dotenv()
    token = os.environ['SJ_TOKEN']

    hh_salary_statistics = dict()
    sj_salary_statistics = dict()

    for language in POPULAR_PROGRAMMING_LANGUAGES:
        vacancy_name = f'Программист {language}'

        try:
            hh_salary = get_hh_salary_statistics(vacancy_name, HH_URL, PERIOD_PLACEMENT)
            sj_salary = get_sj_salary_statistics(vacancy_name, SP_URL, token, PERIOD_PLACEMENT)

        except requests.exceptions.HTTPError as errh:
            logging.error(errh, exc_info=True)

        except requests.exceptions.ConnectionError as errc:
            logging.error(errc, exc_info=True)
            time.sleep(2)
            continue

        except ZeroDivisionError as errz:
            logging.error(errz, exc_info=True)

        hh_salary_statistics[language] = hh_salary
        sj_salary_statistics[language] = sj_salary

    sj_title = 'SuperJob Moscow'
    hh_title = 'HeadHunter Moscow'

    print(make_table(hh_salary_statistics, hh_title))
    print(make_table(sj_salary_statistics, sj_title))

if __name__ == '__main__':
    main()