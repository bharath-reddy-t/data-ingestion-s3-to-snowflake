create or replace transient table {{ params.table_name }}
    (
        department_id int,
        department_name varchar(30)
    );