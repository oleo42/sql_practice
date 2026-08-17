#!/usr/bin/env python3
"""Create the practice database with sample data."""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "practice.db")

if os.path.exists(DB):
    os.remove(DB)

conn = sqlite3.connect(DB)
cur = conn.cursor()

# ── Schema ──────────────────────────────────────────────────────
cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE departments (
    id        INTEGER PRIMARY KEY,
    name      TEXT    NOT NULL,
    location  TEXT    NOT NULL,
    budget    REAL    NOT NULL
);

CREATE TABLE employees (
    id            INTEGER PRIMARY KEY,
    name          TEXT    NOT NULL,
    email         TEXT    NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    manager_id    INTEGER REFERENCES employees(id),
    salary        REAL    NOT NULL,
    hire_date     TEXT    NOT NULL,
    role          TEXT    NOT NULL
);

CREATE TABLE customers (
    id          INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    email       TEXT,
    city        TEXT,
    signup_date TEXT NOT NULL
);

CREATE TABLE products (
    id       INTEGER PRIMARY KEY,
    name     TEXT    NOT NULL,
    category TEXT,
    price    REAL    NOT NULL,
    stock    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    product_id  INTEGER NOT NULL REFERENCES products(id),
    quantity    INTEGER NOT NULL,
    unit_price  REAL    NOT NULL,
    order_date  TEXT    NOT NULL,
    status      TEXT    NOT NULL DEFAULT 'pending'
);
""")

# ── Data ─────────────────────────────────────────────────────────
departments = [
    (1, 'Engineering',   'New York',    950000),
    (2, 'Marketing',     'San Francisco',400000),
    (3, 'Sales',         'Chicago',      600000),
    (4, 'HR',            'New York',     200000),
    (5, 'Finance',       'New York',     350000),
]
cur.executemany("INSERT INTO departments VALUES (?,?,?,?)", departments)

employees = [
    (1,  'Alice Chen',    'alice@co.com',  1, None, 150000, '2019-03-15', 'CTO'),
    (2,  'Bob Martinez',  'bob@co.com',    1, 1,     95000, '2020-06-01', 'Senior Engineer'),
    (3,  'Carol Smith',   'carol@co.com',  1, 2,     82000, '2021-01-10', 'Engineer'),
    (4,  'Diana Lee',     'diana@co.com',  1, 2,     72000, '2022-04-20', 'Junior Engineer'),
    (5,  'Ed Johnson',    'ed@co.com',     2, None,  110000, '2019-11-01', 'VP Marketing'),
    (6,  'Fiona Brown',   'fiona@co.com',  2, 5,     68000, '2020-08-15', 'Marketing Lead'),
    (7,  'George Kim',    'george@co.com', 2, 5,     55000, '2021-09-01', 'Marketing Analyst'),
    (8,  'Hannah Wu',     'hannah@co.com', 3, None,  120000, '2018-05-20', 'VP Sales'),
    (9,  'Ian Davis',     'ian@co.com',    3, 8,     78000, '2020-02-10', 'Sales Manager'),
    (10, 'Julia Patel',   'julia@co.com',  3, 9,     62000, '2021-07-05', 'Sales Rep'),
    (11, 'Kevin Nguyen',  'kevin@co.com',  3, 9,     59000, '2022-11-15', 'Sales Rep'),
    (12, 'Laura Adams',   'laura@co.com',  4, None,  75000, '2020-03-01', 'HR Director'),
    (13, 'Mike Wilson',   'mike@co.com',   4, 12,    48000, '2021-06-20', 'HR Coordinator'),
    (14, 'Nina Thomas',   'nina@co.com',   5, None,  105000, '2019-08-01', 'CFO'),
    (15, 'Oscar White',   'oscar@co.com',  5, 14,    65000, '2022-01-10', 'Accountant'),
]
cur.executemany("INSERT INTO employees VALUES (?,?,?,?,?,?,?,?)", employees)

customers = [
    (1, 'TechCorp',     'info@techcorp.com',  'New York',       '2020-01-15'),
    (2, 'GreenBuild',   'hello@greenb.co',    'San Francisco',  '2020-03-20'),
    (3, 'DataFlow Inc', 'sales@dataflow.io',  'Chicago',        '2021-06-01'),
    (4, 'MediCore',     'contact@medicore',   'Boston',         '2021-09-12'),
    (5, 'RetailMax',    'support@retailmax',  'New York',       '2022-02-28'),
    (6, 'CloudNine',    'dev@cloudnine.io',   'Austin',         '2022-05-15'),
    (7, 'SafeNet',      'ops@safenet.com',    'Seattle',        '2023-01-10'),
    (8, 'EcoSys',       'press@ecosys.org',   'Portland',       '2023-04-22'),
]
cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers)

products = [
    (1, 'Widget Pro',    'Widgets',  19.99,  500),
    (2, 'Widget Lite',   'Widgets',   9.99,  800),
    (3, 'Gadget X',      'Gadgets',  49.99,  200),
    (4, 'Gadget Y',      'Gadgets',  79.99,  150),
    (5, 'Super Tool',    'Tools',    129.99,  75),
    (6, 'Mini Tool',     'Tools',     29.99, 300),
    (7, 'Cloud License', 'Services', 999.99,  50),
    (8, 'Support Tier 1','Services', 199.99, 100),
]
cur.executemany("INSERT INTO products VALUES (?,?,?,?,?)", products)

orders = [
    (1, 1, 1, 10,  19.99, '2023-01-10', 'delivered'),
    (2, 1, 7, 2,  999.99, '2023-01-10', 'delivered'),
    (3, 2, 3, 5,   49.99, '2023-01-15', 'delivered'),
    (4, 3, 5, 3,  129.99, '2023-02-01', 'delivered'),
    (5, 4, 2, 50,   9.99, '2023-02-10', 'delivered'),
    (6, 5, 6, 20,  29.99, '2023-03-05', 'delivered'),
    (7, 1, 4, 8,   79.99, '2023-03-20', 'shipped'),
    (8, 6, 1, 15,  19.99, '2023-04-01', 'shipped'),
    (9, 7, 7, 1,  999.99, '2023-04-10', 'pending'),
    (10, 2, 6, 10, 29.99, '2023-04-15', 'pending'),
    (11, 8, 8, 12,199.99, '2023-05-01', 'pending'),
    (12, 3, 3, 8,  49.99, '2023-05-10', 'shipped'),
    (13, 5, 4, 4,  79.99, '2023-05-20', 'delivered'),
    (14, 4, 5, 2, 129.99, '2023-06-01', 'shipped'),
    (15, 6, 2, 25,  9.99, '2023-06-10', 'pending'),
]
cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", orders)

conn.commit()
conn.close()
print(f"Database created: {DB} ({os.path.getsize(DB)} bytes)")
print("Tables: departments, employees, customers, products, orders")
