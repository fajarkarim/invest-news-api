from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

with DAG(
    "babypips_to_landing",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)        
    },
    description='simple pipeline to put scrape result to staging data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 9, 4),
    catchup=False,
    tags=['source_to_landing'],
) as dag:
    scrape_babypips_calendar = BashOperator(
        task_id="scrape_babypips_calendar",
        bash_command='cat /Users/fajarabdulkarim/learn/data_engineering/invest-news-api/scripts/babypips_scraper.py',
    )

    check_scrape_result = BashOperator(
        task_id = "check_scrape_result",
        bash_command ="date"
    )

    upload_to_bigquery = BashOperator(
        task_id = "upload_to_bigquery",
        bash_command = 'date',
    )

    check_data_source = BashOperator(
        task_id = "check_data_source",
        bash_command = "date"
    )

    stg_calendar_news = BashOperator(
        task_id= "stg_calendar_news",
        bash_command = "date"
    )

    scrape_babypips_calendar >> check_scrape_result >> upload_to_bigquery >> check_data_source >> stg_calendar_news
    