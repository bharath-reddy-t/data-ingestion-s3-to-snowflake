import re
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

# Define your S3 bucket name and regex pattern
BUCKET_NAME = 'api-data-snf'
REGEX_PATTERN = r'demo*'
S3_CONN_ID = 's3_conn'

def list_matching_files():
    s3 = S3Hook(aws_conn_id=S3_CONN_ID)
    files = s3.list_keys(bucket_name=BUCKET_NAME, prefix="demo/")
    matching_files = [f for f in files if re.match(REGEX_PATTERN, f)]
    return matching_files

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('list_matching_files_s3',
         default_args=default_args,
         schedule_interval=timedelta(days=1),
         catchup=False) as dag:

    list_files_task = PythonOperator(
        task_id='list_files_task',
        python_callable=list_matching_files
    )

    list_files_task
