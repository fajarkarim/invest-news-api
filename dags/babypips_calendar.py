from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from fajar.invest_news_api.babypips_scraper import scrape
from fajar.invest_news_api.upload_csv_to_bq import uploadCsv
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor

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

    extract_babypips_calendar = PythonOperator(
        task_id="extract_babypips_calendar",
        python_callable=scrape,
        provide_context=True,
        op_kwargs={
            "nextWeekParam" : "{{ task_instance.xcom_pull(task_ids='get_week_param') }}"
        }
    )

    check_scrape_result = GCSObjectExistenceSensor(
        task_id="check_scrape_result",
        bucket="stoked-brand-360411",
        object="{{ task_instance.xcom_pull(task_ids='extract_babypips_calendar') }}",
        google_cloud_conn_id="gcs_credential",
        mode='poke',
    )

    load_to_bigquery = PythonOperator(
        task_id = "load_to_bigquery",
        python_callable = uploadCsv,
        provide_context=True,
        op_kwargs={
            "csvName" : "{{ task_instance.xcom_pull(task_ids='extract_babypips_calendar') }}"
        }
    )

    check_stg_data = BashOperator(
        task_id = "check_stg_data",
        bash_command = "date"
    )

    stg_calendar_news = BashOperator(
        task_id= "stg_calendar_news",
        bash_command = "date"
    )

    get_week_param >> extract_babypips_calendar >> check_scrape_result >> load_to_bigquery >> stg_calendar_news >> check_stg_data
    