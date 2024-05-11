from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from config import POSTGRES_CONN_ID, POSTGRES_TABLE_NAME
from datetime import datetime

default_args = {
    "owner": "ibbvs",
    "depends_on_past": False,
    "start_date": datetime(2024, 5, 10),
    "retries": 0,
}

dag = DAG("create_stg", default_args=default_args, schedule_interval=None)

create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {POSTGRES_TABLE_NAME} (
        id VARCHAR(255) PRIMARY KEY,
        premium BOOLEAN,
        name VARCHAR(255),
        department VARCHAR(255),
        has_test BOOLEAN,
        response_letter_required BOOLEAN,
        area VARCHAR(255),
        salary VARCHAR(255),
        type VARCHAR(255),
        address VARCHAR(255),
        response_url VARCHAR(255),
        sort_point_distance VARCHAR(255),
        published_at TIMESTAMP,
        created_at TIMESTAMP,
        archived BOOLEAN,
        apply_alternate_url VARCHAR(255),
        show_logo_in_search BOOLEAN,
        insider_interview BOOLEAN,
        url VARCHAR(255),
        alternate_url VARCHAR(255),
        relations VARCHAR(255),
        employer VARCHAR(255),
        snippet TEXT,
        contacts VARCHAR(255),
        schedule VARCHAR(255),
        working_days VARCHAR(255),
        working_time_intervals VARCHAR(255),
        working_time_modes VARCHAR(255),
        accept_temporary BOOLEAN,
        professional_roles VARCHAR(255),
        accept_incomplete_resumes BOOLEAN,
        experience VARCHAR(255),
        employment VARCHAR(255),
        adv_response_url VARCHAR(255),
        is_adv_vacancy BOOLEAN,
        adv_context VARCHAR(255),
        branding VARCHAR(255),
        query VARCHAR(255)
    );
"""

create_table_task = PostgresOperator(
    task_id='create_table',
    postgres_conn_id=POSTGRES_CONN_ID,
    sql=create_table_sql,
    dag=dag,
)

create_table_task
