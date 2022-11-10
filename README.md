# Estimate future salary

Gives average salary statistics for 9 popular programming languages using [superjob api ](https://api.superjob.ru/) and [hh api](https://dev.hh.ru/).

## How to install

- Сlone this repository:
```bash
git clone git@github.com:MaxHC-vlop/estimate_future_salary.git
```

 - You must have python3.9 (or higher) installed .

 - Create a virtual environment on directory project:
 ```bash
python3 -m venv env
 ```
- Start the virtual environment:
```bash
. env/bin/activate
```
- Then use pip to install dependencies:
```bash
pip install -r requirements.txt
```
- Create a file in the project directory `.env` :
```bash
touch .env
```

- Create `SJ_TOKEN` variable in `.env` file given by [superjob](https://api.superjob.ru/):

```
SJ_TOKEN='SUPER_SECRET'
```
## Run

```bash
python3 main.py
```
You will see:
```
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Go                    | 174              | 159                 | 232082           |
| C                     | 959              | 909                 | 179446           |
| C#                    | 274              | 244                 | 183940           |
| C++                   | 349              | 322                 | 181206           |
| PHP                   | 521              | 489                 | 168540           |
| Ruby                  | 48               | 42                  | 203964           |
| Python                | 483              | 426                 | 198801           |
| Java                  | 343              | 287                 | 225441           |
| JavaScript            | 861              | 769                 | 180496           |
+-----------------------+------------------+---------------------+------------------+
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Go                    | 6                | 1                   | 300000           |
| C                     | 13               | 6                   | 129250           |
| C#                    | 2                | 1                   | 240000           |
| C++                   | 14               | 4                   | 168000           |
| PHP                   | 21               | 16                  | 146307           |
| Ruby                  | 3                | 1                   | 325000           |
| Python                | 40               | 24                  | 95461            |
| Java                  | 16               | 5                   | 216500           |
| JavaScript            | 43               | 29                  | 95071            |
+-----------------------+------------------+---------------------+------------------+
```