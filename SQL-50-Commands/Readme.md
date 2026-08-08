# 50 SQL Commands Based on Two Tables

## Project Overview

This project contains 50 SQL commands based on two related tables:

1. `employees`
2. `departments`

The project is designed for practicing SQL fundamentals, filtering, sorting, aggregate functions, grouping, joins, subqueries, updates, deletes, CASE expressions, and views.

## Technologies Used

- MySQL
- SQL

## Project Structure

```text
03-SQL-50-Commands/
├── database.sql
├── 50_sql_commands.sql
└── README.md
```

## Tables

### Employees

| Column | Description |
|---|---|
| employee_id | Unique employee ID |
| employee_name | Employee name |
| department_id | Department reference |
| job_role | Employee job role |
| salary | Employee salary |
| hire_date | Joining date |
| city | Employee city |

### Departments

| Column | Description |
|---|---|
| department_id | Unique department ID |
| department_name | Department name |
| location | Department location |

## SQL Topics Covered

The 50 commands include:

- SELECT
- WHERE
- DISTINCT
- ORDER BY
- LIMIT
- LIKE
- IN
- BETWEEN
- Comparison operators
- COUNT
- SUM
- AVG
- MIN
- MAX
- GROUP BY
- HAVING
- INNER JOIN
- LEFT JOIN
- Subqueries
- UPDATE
- INSERT
- DELETE
- CASE
- CREATE VIEW
- CREATE TABLE
- Foreign keys

## How to Run

### Step 1: Install MySQL

Use MySQL Server with MySQL Workbench or another MySQL client.

### Step 2: Create the database

Open `database.sql` and execute it.

It creates:

```text
company_db
├── departments
└── employees
```

### Step 3: Run the commands

Open:

```text
50_sql_commands.sql
```

Make sure the database is selected:

```sql
USE company_db;
```

Then execute the commands individually or as required.

## Learning Objectives

After completing this project, you should understand:

- How to create related SQL tables
- How primary keys and foreign keys work
- How to retrieve and filter records
- How to use aggregate functions
- How to group records
- How to join two tables
- How to use subqueries
- How to modify records
- How to create and use a SQL view

## Important Note

Commands 35-40 modify the database. If you want to preserve the original sample data, run those commands only after practicing the SELECT queries.

## Author

Your Name

## License

This project is created for educational and learning purposes.
