-- ==========================================
-- SQL PROJECT: 50 COMMANDS BASED ON TWO TABLES
-- ==========================================

DROP DATABASE IF EXISTS company_db;
CREATE DATABASE company_db;
USE company_db;

-- TABLE 1: Departments
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL,
    location VARCHAR(50)
);

-- TABLE 2: Employees
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    department_id INT,
    job_role VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE,
    city VARCHAR(50),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Sample data
INSERT INTO departments VALUES
(1, 'IT', 'Hyderabad'),
(2, 'HR', 'Vijayawada'),
(3, 'Finance', 'Bengaluru'),
(4, 'Marketing', 'Chennai'),
(5, 'Sales', 'Visakhapatnam');

INSERT INTO employees VALUES
(101, 'Ravi Kumar', 1, 'Developer', 65000, '2022-06-10', 'Hyderabad'),
(102, 'Priya Sharma', 2, 'HR Executive', 48000, '2021-03-15', 'Vijayawada'),
(103, 'Arjun Reddy', 1, 'Data Analyst', 58000, '2023-01-20', 'Hyderabad'),
(104, 'Sneha Rao', 3, 'Accountant', 52000, '2020-08-12', 'Bengaluru'),
(105, 'Kiran Kumar', 4, 'Marketing Executive', 45000, '2022-11-05', 'Chennai'),
(106, 'Anjali Devi', 5, 'Sales Executive', 42000, '2023-04-18', 'Visakhapatnam'),
(107, 'Vikram Singh', 1, 'Senior Developer', 85000, '2019-07-22', 'Hyderabad'),
(108, 'Meena Patel', 3, 'Financial Analyst', 70000, '2021-09-30', 'Bengaluru'),
(109, 'Rahul Verma', 5, 'Sales Manager', 76000, '2018-02-14', 'Visakhapatnam'),
(110, 'Divya Nair', 2, 'HR Manager', 72000, '2017-05-25', 'Vijayawada');
