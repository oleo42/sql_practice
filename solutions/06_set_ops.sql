-- ==============================================================
-- Set Operations (UNION, INTERSECT, EXCEPT) — Solutions
-- ==============================================================

-- Task 1: UNION — all distinct locations and cities combined
SELECT location FROM departments
UNION
SELECT city FROM customers;

-- Task 2: INTERSECT — cities that are also department locations
SELECT location FROM departments
INTERSECT
SELECT city FROM customers;

-- Task 3: EXCEPT — customers in cities with no department
-- Use a subquery to filter customers by the EXCEPT result
SELECT name, city
FROM customers
WHERE city IN (
    SELECT city FROM customers
    EXCEPT
    SELECT location FROM departments
);

-- Task 4: UNION — all distinct employee roles and product categories
SELECT role FROM employees
UNION
SELECT category FROM products;

-- Bonus B1: Department cities with customer counts (including zero)
-- Count distinct customers to avoid inflating via repeated department rows
SELECT departments.location AS city, COUNT(DISTINCT customers.id) AS customer_count
FROM departments
LEFT JOIN customers ON departments.location = customers.city
GROUP BY departments.location
UNION
SELECT city, 0
FROM customers
WHERE city NOT IN (SELECT location FROM departments)
GROUP BY city
ORDER BY customer_count DESC;
