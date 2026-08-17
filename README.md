# sql_practice

Interactive SQLite practice CLI: 8 graded exercise sets with solutions, task
tracking, hints, error flags, notes, and a persistent progress store.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install prompt_toolkit pygments
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
