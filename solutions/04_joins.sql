-- Solution 04: JOINs
-- Solutions for multi-table queries using INNER JOIN, LEFT JOIN, and self-joins.

-- Task 1: List all orders with customer and product names
SELECT o.id AS order_id, c.name AS customer, p.name AS product, o.quantity, o.order_date
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id;

-- Task 2: Show employees with department and manager names (managers may be null)
SELECT e.name AS employee, d.name AS department, m.name AS manager
FROM employees e
JOIN departments d ON e.department_id = d.id
LEFT JOIN employees m ON e.manager_id = m.id;

-- Task 3: Find customers who have never placed an order
SELECT c.name, c.email
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;

-- Task 4: Count how many times each product has been ordered (include products never ordered)
SELECT p.name, COUNT(o.id) AS times_ordered
FROM products p
LEFT JOIN orders o ON p.id = o.product_id
GROUP BY p.name;

-- Task 5: List employees earning above the average salary in their department
SELECT e.name, e.salary, d.name AS department
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.salary > (SELECT AVG(salary) FROM employees WHERE department_id = e.department_id);
