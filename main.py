import json

from urllib.parse import urljoin

import requests


BASE_URL = 'https://api.hh.ru'


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
            'period': '30'
        }

        response = requests.get(url, params=payload)
        response.raise_for_status()

        x = response.json()

        found_vacancys[language] = x['found']

        if language == 'Python':
            for i in x['items']:
                print(i['salary'])

    print(found_vacancys)

    with open('works.json', "w", encoding='utf-8') as file:
        json.dump(response.json(), file, indent=7, ensure_ascii=False)


if __name__ == '__main__':
    main()