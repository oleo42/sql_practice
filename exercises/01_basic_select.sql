-- =============================================================================
-- LESSON 1: Basic SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, Column Aliases
-- =============================================================================
-- SELECT is the foundation of SQL. It tells the database which columns you
-- want to retrieve from which table.
--
--   SELECT column1, column2 FROM table_name;
--
-- You can filter rows with WHERE, sort them with ORDER BY, limit how many
-- come back with LIMIT, and deduplicate with DISTINCT.  Column aliases
-- (AS) let you rename a column in the result set.
--
-- ── Quick reference ─────────────────────────────────────────────────────────
--     SELECT    ...    choose columns
--     FROM      ...    name the source table
--     WHERE     ...    filter rows (conditions)
--     ORDER BY  ...    sort ASC | DESC
--     LIMIT     ...    keep only N rows
--     DISTINCT  ...    remove duplicate rows
--     AS        ...    give a column a display alias
-- =============================================================================


-- ── Task 1: Show all employees with their name, salary, and role ───────────
-- Write a query that returns the name, salary, and role columns for every
-- employee in the employees table.

-- HINT: Start with SELECT, list the three column names separated by commas,
--       then FROM the table name.



















-- ── Task 2: Show all products with price > $50, ordered by price descending ─
-- Write a query that returns all columns for products whose price is greater
-- than 50.  The results should be sorted from most expensive to cheapest.

-- HINT: Use WHERE price > 50 and ORDER BY price DESC.



















-- ── Task 3: List the 5 most recently hired employees ───────────────────────
-- Write a query that shows the name, hire_date, and role for the five
-- employees with the most recent hire dates.

-- HINT: ORDER BY hire_date DESC to get newest first, then LIMIT 5 to
--       keep only the head of the list.



















-- ── Task 4: Show all distinct job roles in the company ─────────────────────
-- Write a query that lists every unique role found in the employees table.
-- Each role should appear only once.

-- HINT: Place DISTINCT right after SELECT, before the column name.



















-- ── Task 5: Salary range with column alias ─────────────────────────────────
-- Write a query that shows employees whose salary is between $60,000 and
-- $100,000.  Display their name, salary, and role.  Give the salary column
-- the display alias "Annual Salary" (use AS).

-- HINT: WHERE salary BETWEEN 60000 AND 100000 handles the range.  Use
--       salary AS "Annual Salary" for the alias — double quotes let you
--       keep the space in the alias name.


















-- =============================================================================
-- END OF LESSON 1
-- =============================================================================
