-- Aggregate functions (COUNT, SUM, AVG, MIN, MAX) combine multiple rows into
-- a single summary value. GROUP BY splits rows into groups so aggregation runs
-- per group. HAVING filters groups (like WHERE filters rows).
--
-- Order of evaluation: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY

-- Combine aggregate functions with GROUP BY to answer questions about groups.

-- Task 1: How many employees are in each department?
--        Show department name and employee count.
-- HINT: Join employees to departments, GROUP BY department name, use COUNT(*).

-- Task 2: What is the average salary per department?
--        Show department name and average salary (rounded to 2 decimals).
-- HINT: Use AVG(salary) wrapped in ROUND(..., 2), joined with GROUP BY.

-- Task 3: What is the total revenue from delivered orders?
--        Revenue is quantity * unit_price per order row.
-- HINT: Filter WHERE status = 'delivered', then SUM(quantity * unit_price).

-- Task 4: Which product categories have more than 2 products?
--        Show category and product count.
-- HINT: GROUP BY category, use COUNT(*) in SELECT, filter with HAVING COUNT(*) > 2.

-- Task 5: Which department has the highest total salary spend (sum of salaries)?
--        Show department name and total salary. Return only the top department.
-- HINT: SUM(salary), GROUP BY, ORDER BY total DESC, LIMIT 1.
