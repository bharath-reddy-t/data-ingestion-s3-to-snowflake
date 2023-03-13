from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from pendulum import datetime
from datetime import datetime, timedelta
# import scripts.snowflake as sql_stmts

snf_emp_table = "employees"
snf_dept_table = "departments"

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

with DAG("snf_dag",
         start_date = datetime(2023, 3, 10),
         max_active_runs = 1,
         schedule_interval = "@daily",
         default_args = default_args,
         template_searchpath = "dags/scripts/snowflake/",
         catchup = False
         ) as dag:
    
    create_emp_table = SnowflakeOperator(
        task_id="create_emp_table",
        sql="create_employee_table.sql",
        params={"table_name": snf_emp_table},
    )

    create_dept_table = SnowflakeOperator(
        task_id="create_dept_table",
        sql="create_dept_table.sql",
        params={"table_name": snf_dept_table},
    )

    load_emp_table = SnowflakeOperator(
        task_id="load_emp_table",
        sql="load_emp_data.sql",
        params={"table_name": snf_emp_table},
    )

    load_dept_table = SnowflakeOperator(
        task_id="load_dept_table",
        sql="load_dept_data.sql",
        params={"table_name": snf_dept_table},
    )

    create_emp_table >> create_dept_table >> load_emp_table >> load_dept_table