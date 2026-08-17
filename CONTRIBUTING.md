# Contributing

Thanks for taking an interest. This is a learning repo, so the bar is
"does it teach the concept correctly" rather than "is it clever".

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python setup.py     # builds practice.db
python run.py
```

## Adding or editing an exercise

Every exercise file **must** have a solution file with the identical name:

```
exercises/09_indexes.sql   ->   solutions/09_indexes.sql
```

CI fails if that pairing is broken.

Exercise files are parsed by section, so keep the existing shape:

- A header comment block explaining the concept in prose.
- Numbered tasks, each with its requirement stated as a comment.
- A hint comment per task where the concept is non-obvious.

Solution files hold the reference query for each task in the same order.
Solutions must run against the schema built by `setup.py` — CI executes
every statement in `solutions/*.sql` and fails on any SQL error.

## Schema changes

`setup.py` owns the schema and the seed data. If you change row counts,
update the assertions in `.github/workflows/ci.yml` to match, or CI will
fail on the seed-data check.

Keep the dataset small. It exists to make query results easy to verify by
eye, not to be realistic.

## Before opening a PR

```bash
python setup.py
python -m compileall -q run.py setup.py
```

Then confirm your exercise actually works end to end in `run.py`:
`.load <N>`, `.task 1`, run a query, `.check`.

Please do not commit `practice.db` or `progress.json` — both are generated
and already gitignored.

## Style

SQL keywords uppercase, identifiers lowercase. Python follows the existing
file: standard library only for the runner logic, `prompt_toolkit` and
`pygments` for the REPL layer.
