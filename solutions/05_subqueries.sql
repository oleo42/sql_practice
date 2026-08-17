-- Task 1: Find employees earning more than the company average salary
SELECT name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);

-- Task 2: List departments that have no employees assigned
SELECT name FROM departments WHERE id NOT IN (SELECT DISTINCT department_id FROM employees WHERE department_id IS NOT NULL);
-- Alt: SELECT name FROM departments d WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.department_id = d.id);

-- Task 3: Find customers who ordered products priced over $500
SELECT DISTINCT c.name FROM customers c WHERE EXISTS (
    SELECT 1 FROM orders o JOIN products p ON o.product_id = p.id
    WHERE o.customer_id = c.id AND p.price > 500
);

-- Task 4: Show employees who earn the highest salary in their department
SELECT name, salary, department_id FROM employees e WHERE salary = (
    SELECT MAX(salary) FROM employees WHERE department_id = e.department_id
);

-- Task 5: Show employees earning more than the average salary in their department
SELECT name, salary, department_id FROM employees e WHERE salary > (
    SELECT AVG(salary) FROM employees WHERE department_id = e.department_id
);
