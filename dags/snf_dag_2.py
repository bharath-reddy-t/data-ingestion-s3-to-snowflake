from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from pendulum import datetime
from datetime import datetime, timedelta

snf_lineitem_table = "lineitem"
snf_order_table = "orders"

snowflake_conn_id = "snowflake_default"

#default settings applied to all tasks
default_args = {
    "owner": "airflow",
    "snowflake_conn_id": snowflake_conn_id,
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG("snf_dag2",
         start_date = datetime(2023, 3, 10),
         max_active_runs = 1,
         schedule_interval = "@daily",
         default_args = default_args,
         template_searchpath = "/opt/airflow/scripts/snowflake/",
         catchup = False
         ) as dag:
    
    create_lineitem_table = SnowflakeOperator(
        task_id="create_lineitem_table",
        sql="create_lineitem.sql",
        params={"table_name": snf_lineitem_table},
    )

    create_orders_table = SnowflakeOperator(
        task_id="create_orders_table",
        sql="create_orders.sql",
        params={"table_name": snf_order_table},
    )    

    create_lineitem_table >> create_orders_table