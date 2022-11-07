import json

from urllib.parse import urljoin

import requests


BASE_URL = 'https://api.hh.ru'


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


def main():
    work = 'vacancies'

    url = urljoin(BASE_URL, work)

    popular_programming_languages = [
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

    found_vacancys = {}

    for language in popular_programming_languages:

        vacancy = f'Программист {language}'

        payload = {
            'text': vacancy,
            'area': '1',
            'period': '30',
            'only_with_salary': True,
        }

        response = requests.get(url, params=payload)
        response.raise_for_status()

        x = response.json()

        found_vacancys[language] = x['found']

        if language == 'Python':
            for i in x['items']:
                print(i['salary'])
                print(predict_rub_salary(i['salary']))

    print(found_vacancys)

    with open('works.json', "w", encoding='utf-8') as file:
        json.dump(response.json(), file, indent=7, ensure_ascii=False)


if __name__ == '__main__':
    main()