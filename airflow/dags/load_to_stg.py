from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime
from config import QUERY_TITLES, URL, POSTGRES_CONN_ID, POSTGRES_DB_NAME, POSTGRES_TABLE_NAME
import pandas as pd
import requests

default_args = {
    "owner": "ibbvs",
    "depends_on_past": False,
    "start_date": datetime(2024, 5, 10),
    "retries": 1,
}

dag = DAG("parse_and_load_vacancies", default_args=default_args, schedule_interval=None)

def collect_vacancies_data(QUERY_TITLES: list, URL: str) -> pd.DataFrame:
    """
    Функция для сбора данных о вакансиях с сайта по заданным ключевым словам.

    Аргументы:
    - QUERY_TITLES (list): Список ключевых слов для поиска вакансий.
    - URL (str): URL-адрес сайта для запроса.

    Возвращает:
    - pd.DataFrame: DataFrame с данными о вакансиях.
    """

    # Создаем пустой DataFrame для хранения данных
    df = pd.DataFrame()

    # Итерируемся по списку ключевых слов для вакансий
    for area in range(1, 4):
        for job in QUERY_TITLES:
            # Параметры запроса
            params = {
                "text": job,    # Поиск по ключевому слову
                "area": area,      # Область поиска (Москва)
                "per_page": 100 # Количество вакансий на странице
            }

            # Отправляем запрос
            response = requests.get(URL, params=params)
            data = response.json()

            # Преобразуем полученные данные в DataFrame
            job_df = pd.DataFrame(data["items"])

            # Добавляем столбец с ключевым словом вакансии
            job_df["query"] = job

            # Добавляем данные в общий DataFrame
            df = pd.concat([df, job_df], ignore_index=True)

    return df



def parse_and_load_vacancies():
    # Создаем подключение к PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

    # Выгружаем id вакансий из таблицы в DataFrame
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM {POSTGRES_TABLE_NAME}")
    existing_vacancies = cursor.fetchall()
    existing_ids = [row[0] for row in existing_vacancies]

    # Собираем данные о вакансиях с API
    vacancies_df = collect_vacancies_data(QUERY_TITLES=QUERY_TITLES, URL=URL)

    # Фильтруем дубликаты
    vacancies_df = vacancies_df[~vacancies_df['id'].isin(existing_ids)]

    columns = ", ".join(vacancies_df.columns)
    values = [tuple(row) for row in vacancies_df.values]

    # Загружаем данные в таблицу stg_vacancies
    pg_hook.run(f"""
        INSERT INTO {POSTGRES_TABLE_NAME} ({columns})
        VALUES ({', '.join(['%s'] * len(vacancies_df.columns))});
    """, parameters=values)

parse_task = PythonOperator(
    task_id='parse_and_load_vacancies',
    python_callable=parse_and_load_vacancies,
    dag=dag,
)

parse_task
