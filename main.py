import json

from urllib.parse import urljoin

import requests


BASE_URL = 'https://api.hh.ru'

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


def predict_rub_salary(vacancy):
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


def get_response(url, payload=None):
    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response


def main():
    work = 'vacancies'

    url = urljoin(BASE_URL, work)

    salary_statistics = {}

    for language in POPULAR_PROGRAMMING_LANGUAGES:
        vacancy = f'Программист {language}'
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
                if predict_rub_salary(item['salary']):
                    average_salary += predict_rub_salary(item['salary'])
                    vacancies_processed += 1
        
        average_salary = int(average_salary / vacancies_processed)
        vacancies_found = response['found']

        language_statistics = {
                "vacancies_found": vacancies_found,
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary,
            }
        
        salary_statistics[language] = language_statistics


    print(salary_statistics)


if __name__ == '__main__':
    main()