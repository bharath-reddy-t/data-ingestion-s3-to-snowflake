create or replace table {{ params.table_name }}
as select * from "SNOWFLAKE_SAMPLE_DATA"."TPCH_SF100"."ORDERS" limit 1000;