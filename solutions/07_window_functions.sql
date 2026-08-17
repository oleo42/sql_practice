-- ============================================
-- Solution: Window Functions
-- ============================================

-- Task 1: Rank employees by salary within their department
SELECT name, department_id, salary,
       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_salary_rank
FROM employees;

-- Task 2: Each employee's salary as a percentage of their department total
SELECT name, salary, department_id,
       ROUND(salary * 100.0 / SUM(salary) OVER (PARTITION BY department_id), 1) AS pct_of_dept
FROM employees;

-- Task 3: Show the next lower salary in the same department
SELECT name, salary, department_id,
       LEAD(salary) OVER (PARTITION BY department_id ORDER BY salary DESC) AS next_lower_salary
FROM employees;

-- Task 4: Running total of revenue ordered by date
SELECT id, order_date, quantity * unit_price AS revenue,
       SUM(quantity * unit_price) OVER (ORDER BY order_date) AS running_total
FROM orders;

-- Task 5: Top 2 highest-paid employees per department
SELECT name, department_id, salary FROM (
    SELECT name, department_id, salary,
           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn
    FROM employees
) WHERE rn <= 2;
