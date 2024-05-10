from airflow.models.connection import Connection
from airflow import settings
from config import POSTGRES_CONN_ID, POSTGRES_CONN_TYPE, POSTGRES_HOST, POSTGRES_LOGIN, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_SCHEMA

def create_postgres_connection():
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

if __name__ == "__main__":
    create_postgres_connection()
