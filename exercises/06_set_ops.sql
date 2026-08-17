-- ==============================================================
-- Set Operations: UNION, UNION ALL, INTERSECT, EXCEPT
-- ==============================================================
-- Set operators combine results from two or more SELECT queries
-- into a single result set. Each SELECT must have the same number
-- of columns with compatible types.
--
--   UNION      — combines results, removing duplicate rows
--   UNION ALL  — combines results, keeping all rows (faster!)
--   INTERSECT  — returns only rows present in BOTH result sets
--   EXCEPT     — returns rows from the first set NOT in the second
--
-- SQLite uses EXCEPT (not MINUS). UNION and UNION ALL are the
-- most common; INTERSECT and EXCEPT are useful for diff-style
-- comparisons between tables.
-- ==============================================================

-- ------------------------------------------------------------------
-- Task 1: List all cities where we have either a department location
--         OR a customer. (Use UNION.)
-- HINT: SELECT location FROM departments UNION SELECT city FROM customers
-- ------------------------------------------------------------------

-- Your SQL here



-- ------------------------------------------------------------------
-- Task 2: Find all cities that are both a department location AND
--         have at least one customer. (Use INTERSECT.)
-- HINT: INTERSECT returns rows common to both queries.
-- ------------------------------------------------------------------

-- Your SQL here



-- ------------------------------------------------------------------
-- Task 3: Which customers are located in cities where we do NOT have
--         a department? Show customer name and city. (Use EXCEPT
--         with customer cities vs department locations, then join.)
-- HINT: Filter customers to only those whose city appears in the
--       EXCEPT result — use a subquery or a CTE.
-- ------------------------------------------------------------------

-- Your SQL here



-- ------------------------------------------------------------------
-- Task 4: Combine all employee roles and product categories into one
--         unified list. (Use UNION of distinct roles and categories.)
-- HINT: SELECT role FROM employees UNION SELECT category FROM products
-- ------------------------------------------------------------------

-- Your SQL here


-- ==============================================================
-- Bonus Challenge:
-- ------------------------------------------------------------------
-- Task B1: Show how many customers are in each department city.
--         Use UNION to ensure department cities with zero customers
--         also appear (showing 0).
-- HINT: UNION a grouped count with a list of missing cities
--       padded with 0.
-- ------------------------------------------------------------------
