create or replace table {{ params.table_name }} cluster by (L_SHIPDATE) 
as select * from "SNOWFLAKE_SAMPLE_DATA"."TPCH_SF100"."LINEITEM" limit 500;