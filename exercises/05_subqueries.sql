-- ============================================
-- Exercise: Subqueries
-- ============================================
-- A subquery is a query nested inside another query.
-- Subqueries can appear in SELECT, FROM, WHERE, and HAVING clauses.
--
-- Types covered here:
--   Scalar subquery  — returns a single value (one row, one column)
--   Row subquery     — returns a single row (multiple columns)
--   Table subquery   — returns multiple rows/columns (used in FROM/IN/EXISTS)
--   Correlated       — references columns from the outer query
-- ============================================

-- Task 1: Find employees who earn more than the average salary of ALL employees.
--        Use a scalar subquery in the WHERE clause.
-- HINT:  SELECT AVG(salary) FROM employees returns the overall average.
--        Compare each employee's salary against it using WHERE salary > (subquery).


-- Task 2: Find departments that have no employees assigned.
--        Use NOT EXISTS with a correlated subquery, or NOT IN with a subquery.
-- HINT:  The subquery filters employees WHERE department_id = departments.id.
--        NOT EXISTS is often clearer when the subquery references the outer table.


-- Task 3: Find customers who ordered a product priced over $500.
--        Use EXISTS with a correlated subquery that joins orders to products.
-- HINT:  EXISTS (SELECT 1 FROM orders JOIN products ... WHERE orders.customer_id = customers.id AND products.price > 500)


-- Task 4: Find the highest-paid employee in each department.
--        Use a subquery in WHERE that computes the max salary per department.
-- HINT:  SELECT department_id, MAX(salary) FROM employees GROUP BY department_id
--        Then join the outer employee row on both department_id and salary.


-- Task 5: Find employees whose salary is above their own department's average.
--        This is a correlated subquery — the inner query references the outer row's department_id.
-- HINT:  WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.department_id = e1.department_id)
