from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from config import POSTGRES_CONN_ID, POSTGRES_SCHEMA
from datetime import datetime

default_args = {
    "owner": "ibbvs",
    "depends_on_past": False,
    "start_date": datetime(2024, 5, 10),
    "retries": 0,
}

dag = DAG("check_db_connection", default_args=default_args, schedule_interval=None)

def check_db_connection():
    try:
        # Подключение к базе данных
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID, schema=POSTGRES_SCHEMA)
        return 1
    except Exception as e:
        # Если произошла ошибка при подключении, выводим информацию об ошибке
        print(f"Error while connecting to the database: {str(e)}")

check_task = PythonOperator(
    task_id='check_db_connection',
    python_callable=check_db_connection,
    dag=dag,
)

check_task
