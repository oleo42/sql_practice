--------------------------------------------------------------------------------
-- Solutions for Exercise 02 — Filtering rows with WHERE, IN, LIKE, BETWEEN
--------------------------------------------------------------------------------

-- Task 1: Select employees in department_id 1 (Engineering) or 5 (Finance)
SELECT name, role, salary, department_id FROM employees WHERE department_id IN (1, 5);

-- Task 2: Select products whose category is 'Widgets' or 'Gadgets'
SELECT id, name, category, price FROM products WHERE category IN ('Widgets', 'Gadgets');

-- Task 3: Select customers whose name contains 'tech' or 'data'
SELECT id, name, email FROM customers WHERE name LIKE '%tech%' OR name LIKE '%data%';

-- Task 4: Select orders with status 'pending' or 'shipped'
SELECT id, customer_id, product_id, status, order_date FROM orders WHERE status IN ('pending', 'shipped');

-- Task 5: Select employees hired in 2020 earning more than 60,000
SELECT name, role, salary, hire_date FROM employees WHERE hire_date BETWEEN '2020-01-01' AND '2020-12-31' AND salary > 60000;
