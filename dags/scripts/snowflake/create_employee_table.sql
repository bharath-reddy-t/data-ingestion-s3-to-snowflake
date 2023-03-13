create or replace transient table {{ params.table_name }}
    (
        employee_id int,
        employee_name varchar(20),
        department_id int,
        designation varchar(30),
        salary int,
        location varchar(20)
    );