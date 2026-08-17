-- Task 1: Use a CTE to find employees earning more than $90,000, ordered by salary descending
WITH high_earners AS (
    SELECT name, salary, role FROM employees WHERE salary > 90000
)
SELECT * FROM high_earners ORDER BY salary DESC;

-- Task 2: Use a CTE to find the department with the highest average salary
WITH dept_avg AS (
    SELECT d.name, AVG(e.salary) AS avg_salary
    FROM departments d JOIN employees e ON d.id = e.department_id
    GROUP BY d.name
)
SELECT name, ROUND(avg_salary, 0) AS avg_salary FROM dept_avg ORDER BY avg_salary DESC LIMIT 1;

-- Task 3: Use a recursive CTE to build the employee org chart (manager → reports)
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 0 AS level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, ot.level + 1
    FROM employees e JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT level, name, id FROM org_tree ORDER BY level, name;

-- Task 4: Use a CTE to compute monthly revenue from all orders, sorted by highest revenue
WITH monthly_revenue AS (
    SELECT strftime('%Y-%m', order_date) AS month,
           SUM(quantity * unit_price) AS revenue
    FROM orders
    GROUP BY month
)
SELECT * FROM monthly_revenue ORDER BY revenue DESC;
