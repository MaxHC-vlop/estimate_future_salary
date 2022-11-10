import os

from urllib.parse import urljoin

import requests

from dotenv import load_dotenv
from terminaltables import AsciiTable


HH_URL = 'https://api.hh.ru'
SP_URL = 'https://api.superjob.ru/2.0/'

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


def predict_rub_salary_hh(vacancy) -> None|int:
    if vacancy['currency'] == 'RUR':
        if vacancy['from'] and vacancy['to']:
            average_salary = int((vacancy['from'] + vacancy['to'])/2)

            return average_salary

        if vacancy['from'] and not vacancy['to']:
            average_salary = int(vacancy['from'] * 1.2)

            return average_salary

        if not vacancy['from'] and vacancy['to']:
            average_salary = int(vacancy['to'] * 0.8)

            return average_salary

    return None


def get_hh_salary_statistics(vacancy: str, url: str) -> dict:
    payload = {
            'text': vacancy,
            'area': '1',
            'period': '30',
            'only_with_salary': True,
            'per_page': 100,
        }

    response = get_response(url, payload)
    response = response.json()

    average_salary = 0
    vacancies_processed = 0

    pages = response['pages']

    for page in range(pages):
        payload['page'] = page

        response = get_response(url, payload)
        response = response.json()
    
        for item in response['items']:
            if predict_rub_salary_hh(item['salary']):
                average_salary += predict_rub_salary_hh(item['salary'])
                vacancies_processed += 1
    
    average_salary = int(average_salary / vacancies_processed)
    vacancies_found = response['found']

    language_statistics = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary,
        }

    return language_statistics


def predict_rub_salary_sj(vacancy):
    if vacancy['payment_from'] and vacancy['payment_to']:
        average_salary = int((vacancy['payment_from'] + vacancy['payment_to'])/2)

        return average_salary

    if vacancy['payment_from'] and not vacancy['payment_to']:
        average_salary = int(vacancy['payment_from'] * 1.2)

        return average_salary

    if not vacancy['payment_from'] and vacancy['payment_to']:
        average_salary = int(vacancy['payment_to'] * 0.8)

        return average_salary

    return None


def get_sj_salary_statistics(vacancy: str, url: str) -> dict:
    payload = {
        'town': 'Москва',
        'keyword': vacancy,
        'period': '30',
        "currency": "rub",
        'count': 100
    }
    token = os.environ['SJ_TOKEN']
    headers = {
        'X-Api-App-Id': token,
    }

    response = get_response(url, payload, headers)
    response = response.json()

    average_salary = 0
    vacancies_processed = 0

    vacancies_found = response['total']

    response = get_response(url, payload, headers)
    response = response.json()

    for item in response['objects']:
        if predict_rub_salary_sj(item):
            average_salary += predict_rub_salary_sj(item)
            vacancies_processed += 1
    
    average_salary = int(average_salary / vacancies_processed)

    language_statistics = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary,
        }

    return language_statistics


def get_response(url: str, payload: dict=None, headers: dict=None) -> requests:
    response = requests.get(url, params=payload, headers=headers)
    response.raise_for_status()

    return response


def make_table(salary_statistics, title):
    column_names = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
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
    method = 'vacancies'

    hh_url = urljoin(HH_URL, method)
    sj_url = urljoin(SP_URL, method)

    load_dotenv()

    hh_salary_statistics = dict()
    sj_salary_statistics = dict()

    for language in POPULAR_PROGRAMMING_LANGUAGES:
        vacancy = f'Программист {language}'
        hh_salary_statistics[language] = get_hh_salary_statistics(vacancy, hh_url)
        sj_salary_statistics[language] = get_sj_salary_statistics(vacancy, sj_url)

    sj_title = 'SuperJob Moscow'
    hh_title = 'HeadHunter Moscow'

    print(make_table(hh_salary_statistics, hh_title))
    print(make_table(sj_salary_statistics, sj_title))

if __name__ == '__main__':
    main()