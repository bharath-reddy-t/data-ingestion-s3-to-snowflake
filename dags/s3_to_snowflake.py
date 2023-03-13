from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from datetime import datetime, timedelta
import os
import requests

S3_CONN_ID = 's3_conn'
BUCKET = 'api-data-snf'

def upload_to_s3(endpoint, date):
    s3_hook = S3Hook(aws_conn_id=S3_CONN_ID)
    url = 'https://api.covidtracking.com/v2/states/'
    res = requests.get(url+'{0}/{1}.csv'.format(endpoint, date))
    s3_hook.load_string(res.text, '{0}_{1}.csv'.format(endpoint, date), bucket_name=BUCKET, replace=True)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

endpoints = ['ca', 'co', 'wa', 'or']
date = '{{ ds_nodash }}'

with DAG('s3_to_snowflake',
         start_date = datetime(2023, 3, 10),
         max_active_runs = 1,
         schedule_interval = "@daily",
         default_args = default_args,
         catchup = False
         ) as dag:
    
    t0 = DummyOperator(task_id='start')

    for endpoint in endpoints:
        generate_files = PythonOperator(
            task_id = 'generate_file_{0}'.format(endpoint),
            python_callable = upload_to_s3,
            op_kwargs = {'endpoint': endpoint, 'date': date}
        )

        snowflake = S3ToSnowflakeOperator(
            task_id = 'upload_{0}_snowflake'.format(endpoint),
            s3_keys = ['{0}_{1}.csv'.format(endpoint, date)],
            stage = 's3_stage',
            table = 'state_data',
            schema = 'dev',
            file_format = 'csvformat',
            snowflake_conn_id = 'snowflake_default'
        )

        t0 >> generate_files >> snowflake



