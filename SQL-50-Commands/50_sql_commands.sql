-- ==========================================
-- 50 SQL COMMANDS BASED ON TWO TABLES
-- MySQL
-- ==========================================

USE company_db;

-- 1. Display all employees
SELECT * FROM employees;

-- 2. Display all departments
SELECT * FROM departments;

-- 3. Select employee names and salaries
SELECT employee_name, salary FROM employees;

-- 4. Employees with salary greater than 60000
SELECT * FROM employees WHERE salary > 60000;

-- 5. Employees with salary less than 50000
SELECT * FROM employees WHERE salary < 50000;

-- 6. Employees from Hyderabad
SELECT * FROM employees WHERE city = 'Hyderabad';

-- 7. Employees whose salary is between 50000 and 70000
SELECT * FROM employees WHERE salary BETWEEN 50000 AND 70000;

-- 8. Employees in IT or HR
SELECT * FROM employees
WHERE department_id IN (1, 2);

-- 9. Employees not in IT
SELECT * FROM employees
WHERE department_id <> 1;

-- 10. Employees whose name starts with R
SELECT * FROM employees
WHERE employee_name LIKE 'R%';

-- 11. Employees whose name ends with a
SELECT * FROM employees
WHERE employee_name LIKE '%a';

-- 12. Employees hired after 2021
SELECT * FROM employees
WHERE hire_date > '2021-12-31';

-- 13. Sort employees by salary ascending
SELECT * FROM employees
ORDER BY salary ASC;

-- 14. Sort employees by salary descending
SELECT * FROM employees
ORDER BY salary DESC;

-- 15. Show the top 5 highest-paid employees
SELECT * FROM employees
ORDER BY salary DESC
LIMIT 5;

-- 16. Count total employees
SELECT COUNT(*) AS total_employees
FROM employees;

-- 17. Find the highest salary
SELECT MAX(salary) AS highest_salary
FROM employees;

-- 18. Find the lowest salary
SELECT MIN(salary) AS lowest_salary
FROM employees;

-- 19. Find the average salary
SELECT AVG(salary) AS average_salary
FROM employees;

-- 20. Find total salary
SELECT SUM(salary) AS total_salary
FROM employees;

-- 21. Count employees by department
SELECT department_id, COUNT(*) AS employee_count
FROM employees
GROUP BY department_id;

-- 22. Average salary by department
SELECT department_id, AVG(salary) AS average_salary
FROM employees
GROUP BY department_id;

-- 23. Departments with average salary above 60000
SELECT department_id, AVG(salary) AS average_salary
FROM employees
GROUP BY department_id
HAVING AVG(salary) > 60000;

-- 24. Rename a column in the result
SELECT employee_name AS name, salary AS monthly_salary
FROM employees;

-- 25. Display unique cities
SELECT DISTINCT city
FROM employees;

-- 26. Join employees with departments
SELECT e.employee_name, d.department_name
FROM employees e
INNER JOIN departments d
ON e.department_id = d.department_id;

-- 27. Show employee name, department and location
SELECT e.employee_name, d.department_name, d.location
FROM employees e
INNER JOIN departments d
ON e.department_id = d.department_id;

-- 28. Show employees in the IT department
SELECT e.employee_name, e.job_role, e.salary
FROM employees e
INNER JOIN departments d
ON e.department_id = d.department_id
WHERE d.department_name = 'IT';

-- 29. Show employees and department names ordered by salary
SELECT e.employee_name, d.department_name, e.salary
FROM employees e
INNER JOIN departments d
ON e.department_id = d.department_id
ORDER BY e.salary DESC;

-- 30. Count employees in each department by name
SELECT d.department_name, COUNT(e.employee_id) AS employee_count
FROM departments d
LEFT JOIN employees e
ON d.department_id = e.department_id
GROUP BY d.department_name;

-- 31. Average salary for each department by name
SELECT d.department_name, AVG(e.salary) AS average_salary
FROM departments d
INNER JOIN employees e
ON d.department_id = e.department_id
GROUP BY d.department_name;

-- 32. Employees earning above the overall average salary
SELECT *
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 33. Employee with the highest salary
SELECT *
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);

-- 34. Employees in departments located in Hyderabad
SELECT e.employee_name, d.department_name, d.location
FROM employees e
INNER JOIN departments d
ON e.department_id = d.department_id
WHERE d.location = 'Hyderabad';

-- 35. Increase IT employee salaries by 5 percent
UPDATE employees
SET salary = salary * 1.05
WHERE department_id = 1;

-- 36. Update an employee city
UPDATE employees
SET city = 'Hyderabad'
WHERE employee_id = 106;

-- 37. Update a job role
UPDATE employees
SET job_role = 'Senior HR Executive'
WHERE employee_id = 102;

-- 38. Insert a new department
INSERT INTO departments
VALUES (6, 'Research', 'Pune');

-- 39. Insert a new employee
INSERT INTO employees
VALUES (111, 'Nikhil Rao', 6, 'Research Analyst', 60000, '2024-01-10', 'Pune');

-- 40. Delete an employee
DELETE FROM employees
WHERE employee_id = 111;

-- 41. Find employees with salary >= 70000
SELECT employee_name, salary
FROM employees
WHERE salary >= 70000;

-- 42. Use CASE to categorize salaries
SELECT employee_name, salary,
CASE
    WHEN salary >= 70000 THEN 'High'
    WHEN salary >= 50000 THEN 'Medium'
    ELSE 'Low'
END AS salary_category
FROM employees;

-- 43. Find employees hired between two dates
SELECT *
FROM employees
WHERE hire_date BETWEEN '2020-01-01' AND '2023-12-31';

-- 44. Find employees whose role contains 'Manager'
SELECT *
FROM employees
WHERE job_role LIKE '%Manager%';

-- 45. Find the second-highest salary
SELECT MAX(salary) AS second_highest_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- 46. Find the number of employees earning above 60000
SELECT COUNT(*) AS employees_above_60000
FROM employees
WHERE salary > 60000;

-- 47. Show departments having more than one employee
SELECT d.department_name, COUNT(e.employee_id) AS employee_count
FROM departments d
INNER JOIN employees e
ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name
HAVING COUNT(e.employee_id) > 1;

-- 48. Find the highest salary in each department
SELECT d.department_name, MAX(e.salary) AS highest_salary
FROM departments d
INNER JOIN employees e
ON d.department_id = e.department_id
GROUP BY d.department_name;

-- 49. Show employee details with a calculated annual salary
SELECT employee_name, salary, salary * 12 AS annual_salary
FROM employees;

-- 50. Create a view containing employee and department details
CREATE OR REPLACE VIEW employee_department_view AS
SELECT e.employee_id,
       e.employee_name,
       e.job_role,
       e.salary,
       d.department_name,
       d.location
FROM employees e
INNER JOIN departments d
ON e.department_id = d.department_id;

-- Display the view
SELECT * FROM employee_department_view;
