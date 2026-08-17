-- Task 1: List all employees with name, salary, and role
SELECT name, salary, role FROM employees;

-- Task 2: List all products priced over $50, highest price first
SELECT * FROM products WHERE price > 50 ORDER BY price DESC;

-- Task 3: List the 5 most recently hired employees with their hire date and role
SELECT name, hire_date, role FROM employees ORDER BY hire_date DESC LIMIT 5;

-- Task 4: List every distinct job role in the company
SELECT DISTINCT role FROM employees;

-- Task 5: List employees earning between $60,000 and $100,000, show salary as "Annual Salary", sorted ascending
SELECT name, salary AS "Annual Salary", role FROM employees WHERE salary BETWEEN 60000 AND 100000 ORDER BY salary;
