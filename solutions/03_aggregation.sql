-- Task 1: How many employees are in each department?
SELECT d.name AS department, COUNT(*) AS employee_count
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.name;

-- Task 2: What is the average salary per department?
SELECT d.name AS department, ROUND(AVG(e.salary), 2) AS avg_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.name;

-- Task 3: What is the total revenue from delivered orders?
SELECT SUM(quantity * unit_price) AS total_revenue
FROM orders
WHERE status = 'delivered';

-- Task 4: Which product categories have more than 2 products?
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category
HAVING COUNT(*) > 2;

-- Task 5: Which department has the highest total salary spend?
SELECT d.name AS department, SUM(e.salary) AS total_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.name
ORDER BY total_salary DESC
LIMIT 1;
