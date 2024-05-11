from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models.connection import Connection
from airflow import settings
from datetime import datetime
from config import POSTGRES_CONN_ID, POSTGRES_CONN_TYPE, POSTGRES_HOST, POSTGRES_LOGIN, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_SCHEMA

default_args = {
    "owner": "ibbvs",
    "depends_on_past": False,
    "start_date": datetime(2024, 5, 10),
    "retries": 1,
}

dag = DAG("create_postgres_connection_once", default_args=default_args, schedule_interval=None)

def create_connection_once(**kwargs):
    # Новое подключение к PostgreSQL
    new_conn = Connection(
        conn_id=POSTGRES_CONN_ID,
        conn_type=POSTGRES_CONN_TYPE,
        host=POSTGRES_HOST,
        login=POSTGRES_LOGIN,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
        schema=POSTGRES_SCHEMA
    )

    # Добавление подключения в Airflow
    session = settings.Session()
    session.add(new_conn)
    session.commit()
    session.close()

create_task = PythonOperator(
    task_id='create_postgres_connection_once',
    python_callable=create_connection_once,
    dag=dag,
    provide_context=True,
)

create_task
