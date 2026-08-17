-- ==============================================================
-- JOINs — combining data across tables
-- ==============================================================
-- INNER JOIN  → only matching rows from both sides.
-- LEFT JOIN   → all rows from the left table, NULLs where right
--               has no match.
-- Self-join   → joining a table to itself (use table aliases).
-- Multiple joins → chain several JOIN clauses to bring in data
--                  from three or more tables.
-- ==============================================================

-- HINT:
--   orders joins to customers via customer_id, and to products
--   via product_id. Give each table a short alias (o, c, p)
--   to keep the query readable.

-- ==============================================================
-- Task 1: List all orders with customer name and product name
-- --------------------------------------------------------------
-- Write a 3-table join: orders → customers and orders → products.
-- Show: order_id, customer name, product name, quantity, and
-- order_date.
-- ==============================================================

-- HINT:
--   Join orders to customers ON orders.customer_id = customers.id
--   and orders to products ON orders.product_id = products.id.

-- ==============================================================
-- Task 2: Show all employees with their department name and
--         their manager's name
-- --------------------------------------------------------------
-- Use a self-join on employees: employees.manager_id points to
-- another row in the same table. Use a LEFT JOIN so employees
-- without a manager (e.g. the CTO) still appear.
-- ==============================================================

-- HINT:
--   employees.manager_id = employees.id  (use different aliases:
--   e for the employee, m for the manager).

-- ==============================================================
-- Task 3: Which customers have never placed an order?
-- --------------------------------------------------------------
-- LEFT JOIN customers to orders, then filter where the order
-- columns are NULL. Customers with no matching order rows will
-- have NULL in every orders column.
-- ==============================================================

-- HINT:
--   LEFT JOIN orders ON customers.id = orders.customer_id
--   WHERE orders.id IS NULL  → only customers without orders.

-- ==============================================================
-- Task 4: Show each product name and how many times it has been
--         ordered (including products with zero orders)
-- --------------------------------------------------------------
-- LEFT JOIN products to orders, GROUP BY product, use COUNT()
-- on an orders column. Products never ordered will show count 0.
-- ==============================================================

-- HINT:
--   COUNT(orders.id) counts only non-NULL order ids — products
--   with no matching orders stay in the result with count 0.

-- ==============================================================
-- Task 5: Find employees who earn more than their department's
--         average salary
-- --------------------------------------------------------------
-- Join employees to departments, then filter with a subquery
-- that computes the average salary only within the same
-- department (a correlated subquery: WHERE department_id = e.department_id).
-- ==============================================================

-- HINT:
--   SELECT AVG(salary) FROM employees WHERE department_id = e.department_id
--   — the "e." refers to the outer query's employee row. Place
--   this in a WHERE clause after the join.
