from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.plugins.scripts import babypips_scraper

with DAG(
    "babypips_to_landing",
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

    def getNextWeekParam( **context):
        currentDate = context["currentDate"]
        print(currentDate)
        currentTime = datetime.strptime(currentDate, "%Y-%m-%d")
        year, week_num, day = currentTime.isocalendar()
        nextWeek = week_num + 1
        nextWeekParam = f"{year}-W{nextWeek}"
        return nextWeekParam
    
    get_week_param = PythonOperator(
        task_id="get_week_param",
        python_callable=getNextWeekParam,
        provide_context=True,
        op_kwargs={
            "currentDate" : "{{ ds }}"
        }
    )

    scrape_babypips_calendar = PythonOperator(
        task_id="scrape_babypips_calendar",
        python_callable=babypips_scraper,
        provide_context=True,
    )

    # scrape_babypips_calendar = BashOperator(
    #     task_id="scrape_babypips_calendar",
    #     bash_command="python /Users/fajarabdulkarim/airflow/dags/scripts/babypips_scraper.py {{ task_instance.xcom_pull(task_ids='get_week_param') }}",
    # )

    check_scrape_result = BashOperator(
        task_id = "check_scrape_result",
        bash_command ="cat /Users/fajarabdulkarim/airflow/dags/scripts/check_file_exist.py {{ task_instance.xcom_pull(task_ids='scrape_babypips_calendar') }}"
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

    get_week_param >> scrape_babypips_calendar >> check_scrape_result >> upload_to_bigquery >> check_data_source >> stg_calendar_news
    