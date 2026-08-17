# sql_practice

[![ci](https://github.com/oleo42/sql_practice/actions/workflows/ci.yml/badge.svg)](https://github.com/oleo42/sql_practice/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Interactive SQLite practice CLI: 8 graded exercise sets with solutions, task
tracking, hints, error flags, notes, and a persistent progress store.

Learn SQL by writing queries and checking them against reference solutions,
with your mistakes and notes persisted so you can review what you got wrong.

## Setup

Requires Python >= 3.10. No database server needed — everything runs on the
bundled SQLite file.

```bash
git clone https://github.com/oleo42/sql_practice.git
cd sql_practice
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python setup.py      # builds practice.db with sample data
python run.py        # start the interactive runner
```

`practice.db` and `progress.json` are generated locally and not tracked.

## Exercises

| # | Topic |
|---|-------|
| 01 | Basic SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, aliases |
| 02 | Advanced filtering — IN, BETWEEN, LIKE, IS NULL, AND/OR |
| 03 | Aggregation — COUNT/SUM/AVG/MIN/MAX, GROUP BY, HAVING |
| 04 | JOINs across tables |
| 05 | Subqueries |
| 06 | Set operations — UNION, UNION ALL, INTERSECT, EXCEPT |
| 07 | Window functions |
| 08 | CTEs and recursive CTEs |

`exercises/` holds the prompts, `solutions/` the reference queries.

## Runner commands

```
.exercises         List all exercises
.load <N|name>     Load exercise N
.info              Exercise description / context

.tasks             List tasks in current exercise
.task <N>          Select task N
.show              Re-show current task requirement
.hint              Hint for current task

.check             Compare last query result against the solution
.solution          Show the solution query
.mark              Toggle error flag
.done              Toggle completion status
.errors            Show marked errors

.note <text>       Attach a note to current task
.notes             Show all notes

.progress          Progress bar across all exercises
.report            Errors + notes for current exercise

.tables            List database tables
.schema [table]    Show table schema

<SQL>              Run any SQL against practice.db
.help  .q
```

## Reusing this

Fork it and add your own exercise sets. Each lesson is a plain `.sql` file
in `exercises/` paired with a same-named file in `solutions/`; the runner
discovers them automatically, so adding lesson 09 needs no code change.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the file format and dev setup.

## License

[MIT](LICENSE) — free to use, modify, and redistribute, including for
teaching and commercial training material.
