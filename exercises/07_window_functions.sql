-- ============================================
-- Exercise: Window Functions
-- ============================================
-- Window functions perform calculations across
-- a set of rows that are related to the current
-- row — without collapsing them into a single
-- output row like GROUP BY does.
--
-- Key functions covered:
--   ROW_NUMBER()     — unique sequential integer per partition
--   RANK()           — rank with gaps for ties
--   DENSE_RANK()     — rank without gaps for ties
--   SUM() / AVG()    — aggregate over a moving window
--   LEAD() / LAG()   — access rows ahead of / behind the current row
--
-- Every window function needs an OVER() clause:
--   OVER (PARTITION BY col ORDER BY col)
-- ============================================

----------------------------------------------------------------------
-- Task 1: Rank employees by salary within their department
--
-- Write a query that shows each employee's name, department_id,
-- salary, and their rank within their department (highest salary
-- ranked #1). Use RANK() so that employees with the same salary
-- get the same rank, leaving a gap in the sequence.
--
-- Columns: name | department_id | salary | dept_salary_rank
-- Ordered by: department_id, salary DESC
----------------------------------------------------------------------

-- HINT: RANK() OVER (PARTITION BY department_id ORDER BY salary DESC)





----------------------------------------------------------------------
-- Task 2: Each employee's salary as percentage of department total
--
-- Show every employee along with the percentage of their
-- department's total salary that their salary represents.
-- Use SUM(salary) OVER (PARTITION BY department_id) and
-- calculate: salary * 100.0 / total *round to 1 decimal place.
--
-- Columns: name | salary | department_id | pct_of_dept
-- Ordered by: department_id, pct_of_dept DESC
----------------------------------------------------------------------

-- HINT: ROUND(salary * 100.0 / SUM(salary) OVER (PARTITION BY department_id), 1)





----------------------------------------------------------------------
-- Task 3: For each employee, show the next lower salary
--         in the same department
--
-- Write a query that shows each employee's name, salary, and the
-- salary of the next *lower-paid* employee in their department.
-- Employees at the bottom (no lower peer) should show NULL.
-- Use LEAD() with ORDER BY salary DESC.
--
-- Columns: name | salary | department_id | next_lower_salary
-- Ordered by: department_id, salary DESC
----------------------------------------------------------------------

-- HINT: LEAD(salary) OVER (PARTITION BY department_id ORDER BY salary DESC)





----------------------------------------------------------------------
-- Task 4: Running total of revenue ordered by date
--
-- Write a query against the orders table that shows each order's
-- revenue (quantity * unit_price) and a running total that
-- accumulates in order-date order.
--
-- Columns: id | order_date | revenue | running_total
-- Ordered by: order_date
----------------------------------------------------------------------

-- HINT: SUM(quantity * unit_price) OVER (ORDER BY order_date)





----------------------------------------------------------------------
-- Task 5: Top 2 highest-paid employees in each department
--
-- Use ROW_NUMBER() in a subquery or CTE to number employees within
-- each department by salary descending, then filter to the top 2.
--
-- Columns: name | department_id | salary
-- Ordered by: department_id, salary DESC
----------------------------------------------------------------------

-- HINT: Wrap ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC)
--       in a subquery, then filter WHERE rn <= 2
