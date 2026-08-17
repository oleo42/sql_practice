#!/usr/bin/env python3
"""
SQL Practice Runner — interactive learning CLI with task management.

Commands:
  .help              Show this help
  .q                 Quit

  .exercises         List all exercises
  .load <N|name>     Load exercise N (e.g. .load 1)
  .info              Show exercise description / context

  .tasks             List all tasks in current exercise
  .task <N>          Select task N, show its requirement
  .show              Show current task requirement again
  .hint              Show hint for current task

  .check             Compare your last query result against the solution
  .solution          Show the solution query for current task
  .mark              Toggle error flag for current task
  .done              Toggle task completion status (✓ / ○)
  .errors            Show all marked errors in current exercise

  .note <text>       Attach a note to current task
  .notes             Show all notes in current exercise

  .progress          Show progress bar across all exercises
  .report            Full review report: errors + notes for current exercise

  .tables            List database tables
  .schema [table]    Show table schema

  <SQL>              Run any SQL query against practice.db
"""

import sqlite3, os, re, sys, textwrap, json
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers import SqlLexer

DB = os.path.join(os.path.dirname(__file__), "practice.db")
EX_DIR = Path(os.path.dirname(__file__)) / "exercises"
SOL_DIR = Path(os.path.dirname(__file__)) / "solutions"

assert os.path.exists(DB), f"Run setup.py first — missing {DB}"

# ── Persistent progress store ─────────────────────────────────────

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "progress.json")


class ProgressStore:
    """Persistent progress: errors + notes saved to JSON on every mutation."""

    def __init__(self, path):
        self.path = path
        self.errors = {}  # {exercise: {task_num: {"query": str, "count": int}}}
        self.notes = {}  # {exercise: {task_num: [str, ...]}}
        self.completed = {}  # {exercise: {task_num: true}}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    data = json.load(f)
                self.errors = data.get("errors", {})
                self.notes = data.get("notes", {})
                self.completed = data.get("completed", {})
                # Normalize any int keys → str (legacy data)
                for d in (self.errors, self.notes, self.completed):
                    for ex in list(d):
                        d[ex] = {str(k): v for k, v in d[ex].items()}
            except (json.JSONDecodeError, OSError):
                pass  # corrupt file → start fresh

    def _save(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(
                {
                    "errors": self.errors,
                    "notes": self.notes,
                    "completed": self.completed,
                },
                f,
                indent=2,
            )
        os.replace(tmp, self.path)  # atomic write

    def mark_error(self, ex, task_num, query):
        tn = str(task_num)
        if ex not in self.errors:
            self.errors[ex] = {}
        if tn not in self.errors[ex]:
            self.errors[ex][tn] = {"query": query, "count": 0}
        self.errors[ex][tn]["count"] += 1
        if query:
            self.errors[ex][tn]["query"] = query
        self._save()

    def unmark_error(self, ex, task_num):
        tn = str(task_num)
        if ex in self.errors and tn in self.errors[ex]:
            del self.errors[ex][tn]
            if not self.errors[ex]:
                del self.errors[ex]
            self._save()

    def add_note(self, ex, task_num, text):
        tn = str(task_num)
        if ex not in self.notes:
            self.notes[ex] = {}
        if tn not in self.notes[ex]:
            self.notes[ex][tn] = []
        self.notes[ex][tn].append(text)
        self._save()

    def mark_completed(self, ex, task_num):
        if ex not in self.completed:
            self.completed[ex] = {}
        self.completed[ex][str(task_num)] = True
        self._save()

    def unmark_completed(self, ex, task_num):
        tn = str(task_num)
        if ex in self.completed and tn in self.completed[ex]:
            del self.completed[ex][tn]
            if not self.completed[ex]:
                del self.completed[ex]
            self._save()

    def is_completed(self, ex, task_num):
        return ex in self.completed and str(task_num) in self.completed[ex]


progress = ProgressStore(PROGRESS_FILE)

# ── Parsing ───────────────────────────────────────────────────────

# ── Parsing ───────────────────────────────────────────────────────────

TASK_RE = re.compile(r"--\s*[-─═]*\s*Task\s+(\d+)", re.IGNORECASE)
SOL_TASK_RE = re.compile(r"--\s*Task\s+(\d+)", re.IGNORECASE)


def parse_exercise(path):
    """Return {title, intro, tasks: [{num, desc_lines, hint_lines}]}."""
    raw = path.read_text()
    lines = raw.splitlines()
    result = {"title": "", "intro": [], "tasks": []}
    # --- Extract title and intro (everything before first Task marker) ---
    task_starts = []
    for i, line in enumerate(lines):
        m = TASK_RE.search(line)
        if m:
            task_starts.append((i, int(m.group(1))))
    if not task_starts:
        return result

    # Title from first non-bar comment line
    for line in lines[:5]:
        s = line.strip()
        if s.startswith("--") and not s.startswith("--=") and not s.startswith("---"):
            clean = s.lstrip("- ").strip()
            if clean and not all(c in "-=─═ " for c in clean):
                result["title"] = clean
                break
    # Intro = lines before first task start (skip title line)
    intro_end = task_starts[0][0]
    seen_title = False
    for line in lines[:intro_end]:
        s = line.strip()
        if s.startswith("--") and not s.startswith("--=") and not s.startswith("---"):
            clean = s.lstrip("- ").strip()
            if clean and not all(c in "-=─═ " for c in clean):
                if not seen_title and clean == result["title"]:
                    seen_title = True
                    continue
                result["intro"].append(clean)

    # ── Tasks ──
    for idx, (start_line, num) in enumerate(task_starts):
        end_line = task_starts[idx + 1][0] if idx + 1 < len(task_starts) else len(lines)
        block = lines[start_line:end_line]

        desc_lines = []
        hint_lines = []
        collecting_desc = True
        saw_content = False
        in_hint = False
        for line in block:
            s = line.strip()
            # First block line is the "Task N:" header — extract content, skip rest
            if line is block[0]:
                m = TASK_RE.search(s)
                if m:
                    content = s[m.end() :].lstrip(": —-\t").rstrip(" -=─═\t")
                    if content:
                        desc_lines.append(content)
                        saw_content = True
                continue
            # Hit a separator bar line  - skip
            stripped = line.strip("- =─═")
            if stripped == "" and s != "":
                in_hint = False
                continue
            # Hit a HINT line — switch to hint collection
            if s.upper().startswith("-- HINT") or s.upper().startswith("--hint"):
                in_hint = True
                collecting_desc = False
                hint_text = s.lstrip("- ").strip()
                if hint_text and hint_text.upper() not in ("HINT", "HINT:"):
                    hint_lines.append(hint_text)
                continue
            # Continue collecting hint content on subsequent comment lines
            if in_hint and s.startswith("--"):
                clean = s.lstrip("- ").strip()
                if clean:
                    hint_lines.append(clean)
                continue
            # Hit a non-comment line — stop entirely
            if not s.startswith("--") and s:
                in_hint = False
                break
            # Comment line while collecting description
            if collecting_desc and s.startswith("--"):
                clean = s.lstrip("- ").strip()
                if clean:
                    desc_lines.append(clean)
                    saw_content = True
            in_hint = False
        result["tasks"].append(
            {
                "num": num,
                "desc_lines": desc_lines,
                "hint_lines": hint_lines,
                "raw_block": block,
            }
        )
    return result


def parse_solution(path):
    """Return {num: query, ...} for each task."""
    if not path.exists():
        return {}
    raw = path.read_text()
    lines = raw.splitlines()
    tasks = {}
    current_num = None
    current_query = []

    for line in lines:
        m = SOL_TASK_RE.search(line)
        if m:
            if current_num is not None and current_query:
                q = " ".join(current_query).strip()
                if q:
                    tasks[current_num] = q
            current_num = int(m.group(1))
            current_query = []
        elif current_num is not None:
            s = line.strip()
            if s and not s.startswith("--"):
                current_query.append(s)
    if current_num is not None and current_query:
        q = " ".join(current_query).strip()
        if q:
            tasks[current_num] = q
    return tasks


# ── Result display ────────────────────────────────────────────────────


def fmt_rows(rows, headers, max_col=36):
    if not rows:
        return "(empty)"
    w = [max(len(h), 6) for h in headers]
    for r in rows:
        for i, v in enumerate(r):
            s = str(v) if v is not None else "NULL"
            w[i] = max(w[i], min(len(s), max_col))
    sep = "+" + "+".join("-" * (wi + 2) for wi in w) + "+"
    out = [sep]
    hdr = "| " + " | ".join(h.center(w[i]) for i, h in enumerate(headers)) + " |"
    out.append(hdr)
    out.append(sep.replace("-", "="))
    for r in rows:
        cells = []
        for i, v in enumerate(r):
            s = str(v) if v is not None else "NULL"
            if len(s) > w[i]:
                s = s[: w[i] - 3] + ".."
            cells.append(s.ljust(w[i]))
        out.append("| " + " | ".join(cells) + " |")
    out.append(sep)
    return "\n".join(out)


# ── Helpers ────────────────────────────────────────────────────────────


def _show_report(ex, exercise_data):
    """Print a full review report for the given exercise."""
    p = progress
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print(f"║  Review Report: {ex:<39} ║")
    print("╠══════════════════════════════════════════════════════════╣")
    task_count = len(exercise_data["tasks"]) if exercise_data else 0
    err_count = len(p.errors.get(ex, {}))
    note_count = sum(len(v) for v in p.notes.get(ex, {}).values())
    done_count = sum(
        1
        for t in (exercise_data["tasks"] if exercise_data else [])
        if p.is_completed(ex, t["num"])
    )
    print(
        f"║  Tasks: {task_count}  |  Done: {done_count}  |  Errors: {err_count}  |  Notes: {note_count}  ║"
    )
    print("╚══════════════════════════════════════════════════════════╝")

    if err_count:
        print()
        print("── Errors ──────────────────────────────────────────────")
        for tn in sorted(p.errors[ex], key=int):
            info = p.errors[ex][tn]
            print(f"  Task {tn}: ✗ ({info['count']}x)")
            print(f"    Query: {info['query'][:100]}")

    if note_count:
        print()
        print("── Notes ───────────────────────────────────────────────")
        for tn in sorted(p.notes[ex], key=int):
            for n in p.notes[ex][tn]:
                print(f"  Task {tn}: • {n}")

    if not err_count and not note_count:
        print("  (nothing recorded)")

    print()


def _build_session():
    """Create a prompt_toolkit PromptSession with SQL highlighting, completion, history, auto-suggest."""
    history_file = os.path.expanduser("~/.sql_practice_history")

    dot_commands = [
        ".check",
        ".done",
        ".errors",
        ".exercises",
        ".help",
        ".hint",
        ".info",
        ".load",
        ".mark",
        ".note",
        ".notes",
        ".progress",
        ".q",
        ".quit",
        ".report",
        ".schema",
        ".show",
        ".solution",
        ".tables",
        ".task",
        ".tasks",
    ]
    sql_keywords = [
        "SELECT",
        "FROM",
        "WHERE",
        "INSERT",
        "INTO",
        "VALUES",
        "UPDATE",
        "SET",
        "DELETE",
        "CREATE",
        "TABLE",
        "DROP",
        "ALTER",
        "ADD",
        "COLUMN",
        "INDEX",
        "VIEW",
        "JOIN",
        "INNER",
        "LEFT",
        "RIGHT",
        "OUTER",
        "FULL",
        "CROSS",
        "ON",
        "AND",
        "OR",
        "NOT",
        "IN",
        "BETWEEN",
        "LIKE",
        "IS",
        "NULL",
        "AS",
        "ORDER",
        "BY",
        "ASC",
        "DESC",
        "GROUP",
        "HAVING",
        "LIMIT",
        "OFFSET",
        "DISTINCT",
        "UNION",
        "ALL",
        "EXISTS",
        "CASE",
        "WHEN",
        "THEN",
        "ELSE",
        "END",
        "COUNT",
        "SUM",
        "AVG",
        "MIN",
        "MAX",
        "OVER",
        "PARTITION",
        "RANK",
        "ROW_NUMBER",
        "LEAD",
        "LAG",
        "FIRST_VALUE",
        "WITH",
        "RECURSIVE",
        "CAST",
        "COALESCE",
        "NULLIF",
    ]

    style = Style.from_dict(
        {
            "prompt": "ansicyan bold",
            "continuation": "ansibrightblack",
        }
    )

    return PromptSession(
        history=FileHistory(history_file),
        auto_suggest=AutoSuggestFromHistory(),
        completer=WordCompleter(dot_commands + sql_keywords, ignore_case=True),
        lexer=PygmentsLexer(SqlLexer),
        style=style,
        complete_while_typing=True,
    )


# ── REPL ──────────────────────────────────────────────────────────────


def repl():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    current_exercise = None  # name stem
    exercise_data = None  # parsed dict
    solution_data = None  # parsed dict
    current_task = None  # task num
    last_query = None  # last SQL the user ran
    session = _build_session()

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║        SQL Practice — Interactive Learning CLI         ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║  Commands: .exercises | .load N | .tasks | .task N     ║")
    print("║            .show | .hint | .check | .solution          ║")
    print("║            .mark | .done | .note | .notes              ║")
    print("║            .errors | .progress | .report               ║")
    print("║            .help | .q                                  ║")
    print("║  SQL syntax highlighted  ·  Tab completes              ║")
    print("║  ↑↓ history · Ctrl+R search · Ctrl+N/P cycle           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    while True:
        try:
            inp = session.prompt("sql> ").strip()
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            print("\nBye!")
            break
        if not inp:
            continue

        # ── Dot commands ────────────────────────────────────────
        if inp.startswith("."):
            parts = inp.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if cmd in (".q", ".quit"):
                print("Bye!")
                break

            elif cmd == ".help":
                print(__doc__)

            elif cmd == ".tables":
                cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                )
                print("Tables:")
                for (n,) in cur.fetchall():
                    print(f"  {n}")

            elif cmd == ".schema":
                if arg:
                    cur.execute(
                        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
                        (arg,),
                    )
                    row = cur.fetchone()
                    print(row[0] if row else f"No table '{arg}'")
                else:
                    cur.execute(
                        "SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name"
                    )
                    for (s,) in cur.fetchall():
                        print(s)
                        print()

            elif cmd == ".exercises":
                exercises = sorted(f.stem for f in EX_DIR.glob("*.sql"))
                print(f"Exercises ({len(exercises)}):")
                for e in exercises:
                    print(f"  {e}")

            elif cmd == ".load":
                if not arg:
                    print("Usage: .load <number or name>")
                    continue

                # Show report for previous exercise before switching
                if current_exercise and (
                    progress.errors.get(current_exercise)
                    or progress.notes.get(current_exercise)
                ):
                    _show_report(current_exercise, exercise_data)
                    print()

                stem = f"{int(arg):02d}_" if arg.isdigit() else arg
                found = sorted(EX_DIR.glob(f"{stem}*.sql"))
                if not found:
                    print(f"Exercise '{arg}' not found. Try .exercises")
                    continue
                name = found[0].stem
                current_exercise = name
                exercise_data = parse_exercise(EX_DIR / f"{name}.sql")
                solution_data = parse_solution(SOL_DIR / f"{name}.sql")
                current_task = None
                last_query = None

                print()
                print("=" * 60)
                print(f"  {exercise_data['title'] or name}")
                print("=" * 60)
                if exercise_data["intro"]:
                    for line in exercise_data["intro"]:
                        if line:
                            print(f"  {line}")
                tasks = exercise_data["tasks"]
                print()
                print(f"  {len(tasks)} tasks. Use .tasks to list, .task <N> to start.")
                print()

            elif cmd == ".info":
                if not exercise_data:
                    print("No exercise loaded. Use .load <N> first.")
                    continue
                print()
                print("=" * 60)
                print(f"  {exercise_data['title'] or current_exercise}")
                print("=" * 60)
                if exercise_data["intro"]:
                    for line in exercise_data["intro"]:
                        if line:
                            print(f"  {line}")
                print()

            elif cmd == ".tasks":
                if not exercise_data:
                    print("No exercise loaded. Use .load <N> first.")
                    continue
                tasks = exercise_data["tasks"]
                print(f"Tasks in {current_exercise}:")
                for t in tasks:
                    # First non-empty desc line as summary
                    summary = ""
                    for d in t["desc_lines"]:
                        if d.strip():
                            summary = d.strip()[:70]
                            break
                    marker = " ← current" if current_task == t["num"] else ""
                    ex = current_exercise
                    tn = t["num"]
                    emoji = ""
                    if progress.is_completed(ex, tn):
                        emoji += " ✓"
                    if ex in progress.errors and tn in progress.errors[ex]:
                        emoji += " ✗"
                    if ex in progress.notes and tn in progress.notes[ex]:
                        emoji += " 📝"
                    print(f"  {t['num']}. {summary}{emoji}{marker}")
                # Summary line
                total = len(tasks)
                done = sum(1 for t in tasks if progress.is_completed(ex, t["num"]))
                errors = sum(
                    1
                    for t in tasks
                    if ex in progress.errors and t["num"] in progress.errors[ex]
                )
                print(f"\n  {done}/{total} completed | {errors} with errors")
                if not current_task:
                    print(f"\nUse .task <N> to select one (1–{len(tasks)}).")

            elif cmd == ".task":
                if not exercise_data:
                    print("No exercise loaded. Use .load <N> first.")
                    continue
                if not arg or not arg.isdigit():
                    print("Usage: .task <number>")
                    continue
                num = int(arg)
                found = [t for t in exercise_data["tasks"] if t["num"] == num]
                if not found:
                    # Try index-based
                    tasks = exercise_data["tasks"]
                    if 1 <= num <= len(tasks):
                        found = [tasks[num - 1]]
                    else:
                        print(f"No task {num} in this exercise.")
                        continue
                t = found[0]
                current_task = t["num"]
                print()
                print(f"── Task {t['num']} ──────────────────────────────────────")
                for d in t["desc_lines"]:
                    print(f"  {d}")
                print(f"──────────────────────────────────────────────────────")
                has_sol = t["num"] in solution_data if solution_data else False
                has_hint = len(t["hint_lines"]) > 0
                tips = []
                if has_hint:
                    tips.append(".hint")
                if has_sol:
                    tips.append(".check after query")
                if tips:
                    print(f"  ({', '.join(tips)})")
                print()

            elif cmd == ".show":
                if current_task is None:
                    print("No task selected. Use .task <N> first.")
                    continue
                # Re-show current task
                tasks = exercise_data["tasks"]
                found = [t for t in tasks if t["num"] == current_task]
                if not found:
                    print("Task data missing — reload with .load")
                    continue
                t = found[0]
                print()
                print(f"── Task {t['num']} ──────────────────────────────────────")
                for d in t["desc_lines"]:
                    print(f"  {d}")
                print(f"──────────────────────────────────────────────────────")
                print()

            elif cmd == ".hint":
                if current_task is None:
                    print("No task selected. Use .task <N> first.")
                    continue
                tasks = exercise_data["tasks"]
                found = [t for t in tasks if t["num"] == current_task]
                if not found or not found[0]["hint_lines"]:
                    print("No hint for this task.")
                    continue
                for h in found[0]["hint_lines"]:
                    print(f"  💡 {h}")

            elif cmd == ".solution":
                if current_task is None:
                    print("No task selected. Use .task <N> first.")
                    continue
                if not solution_data or current_task not in solution_data:
                    print("No solution available for this task.")
                    continue
                print()
                print("--- Solution ---")
                print(f"  {solution_data[current_task]}")
                print()

            elif cmd == ".check":
                if current_task is None:
                    print("No task selected. Use .task <N> first.")
                    continue
                if last_query is None:
                    print("No query to check. Run a SQL query first.")
                    continue
                if not solution_data or current_task not in solution_data:
                    print("No solution available for this task.")
                    continue

                sol_query = solution_data[current_task]
                try:
                    cur.execute(last_query)
                    user_rows = cur.fetchall()
                    user_headers = (
                        [d[0] for d in cur.description] if cur.description else []
                    )
                except Exception as e:
                    print(f"Your query error: {e}")
                    continue

                try:
                    cur.execute(sol_query)
                    sol_rows = cur.fetchall()
                    sol_headers = (
                        [d[0] for d in cur.description] if cur.description else []
                    )
                except Exception as e:
                    print(f"Solution query error (bug): {e}")
                    continue

                # Compare
                print()
                print("── Check Results ────────────────────────────────────")
                print(
                    f"  Your query returned:  {len(user_rows)} rows, {len(user_headers)} cols"
                )
                print(
                    f"  Solution returned:    {len(sol_rows)} rows, {len(sol_headers)} cols"
                )
                print()

                if len(user_rows) != len(sol_rows):
                    print("  ✗ Row count mismatch.")
                    progress.mark_error(current_exercise, current_task, last_query)
                    progress.unmark_completed(current_exercise, current_task)
                elif len(user_headers) != len(sol_headers):
                    print("  ✗ Column count mismatch.")
                    progress.mark_error(current_exercise, current_task, last_query)
                    progress.unmark_completed(current_exercise, current_task)
                elif user_rows == sol_rows and user_headers == sol_headers:
                    print("  ✓ Exact match! Great query.")
                    progress.mark_completed(current_exercise, current_task)
                elif sorted(tuple(r) for r in user_rows) == sorted(
                    tuple(r) for r in sol_rows
                ) and set(user_headers) == set(sol_headers):
                    print("  ✓ Same data (order may differ). Looks good!")
                    progress.mark_completed(current_exercise, current_task)
                elif set(tuple(r) for r in user_rows) == set(
                    tuple(r) for r in sol_rows
                ):
                    print("  ~ Same data, different column order. Still correct.")
                    progress.mark_completed(current_exercise, current_task)
                else:
                    print("  ✗ Data differs from the solution.")
                    progress.mark_error(current_exercise, current_task, last_query)
                    progress.unmark_completed(current_exercise, current_task)
                    user_set = set(tuple(r) for r in user_rows)
                    sol_set = set(tuple(r) for r in sol_rows)
                    missing = sol_set - user_set
                    extra = user_set - sol_set
                    if missing:
                        print(
                            f"     Missing rows (in solution, not in yours): {len(missing)}"
                        )
                        for r in list(missing)[:3]:
                            print(f"       {r}")
                    if extra:
                        print(
                            f"     Extra rows (in yours, not in solution): {len(extra)}"
                        )
                        for r in list(extra)[:3]:
                            print(f"       {r}")
                print()

            elif cmd == ".mark":
                if current_task is None:
                    print("No task selected. Use .task <N> first.")
                    continue
                if not current_exercise:
                    print("No exercise loaded.")
                    continue
                ex = current_exercise
                tn = current_task
                if ex in progress.errors and tn in progress.errors[ex]:
                    progress.unmark_error(ex, tn)
                    print(f"  ✓ Task {tn} unmarked.")
                else:
                    progress.mark_error(ex, tn, last_query or "(no query saved)")
                    print(f"  ⚑ Task {tn} marked as error-prone.")

            elif cmd == ".done":
                if current_task is None:
                    print("No task selected. Use .task <N> first.")
                    continue
                if not current_exercise:
                    print("No exercise loaded.")
                    continue
                ex = current_exercise
                tn = current_task
                if progress.is_completed(ex, tn):
                    progress.unmark_completed(ex, tn)
                    print(f"  ○ Task {tn} marked as incomplete.")
                else:
                    progress.mark_completed(ex, tn)
                    print(f"  ✓ Task {tn} marked as completed.")

            elif cmd == ".errors":
                if not current_exercise:
                    print("No exercise loaded.")
                    continue
                ex = current_exercise
                if ex not in progress.errors or not progress.errors[ex]:
                    print("No errors marked in this exercise.")
                    print()
                    continue
                print(f"── Errors: {ex} ─────────────────────────────────")
                for tn in sorted(progress.errors[ex], key=int):
                    info = progress.errors[ex][tn]
                    print(f"  Task {tn}: ✗ ({info['count']}x)")
                    print(f"    Query: {info['query'][:80]}")
                print()
            elif cmd == ".note":
                if current_task is None:
                    print("No task selected. Use .task <N> first.")
                    continue
                if not current_exercise:
                    print("No exercise loaded.")
                    continue
                if not arg:
                    print("Usage: .note <your note text>")
                    continue
                progress.add_note(current_exercise, current_task, arg)
                print(f"  ✓ Note saved for Task {current_task}.")
                print()

            elif cmd == ".notes":
                if not current_exercise:
                    print("No exercise loaded.")
                    continue
                ex = current_exercise
                if ex not in progress.notes or not progress.notes[ex]:
                    print("No notes in this exercise.")
                    print()
                    continue
                print(f"── Notes: {ex} ──────────────────────────────────")
                for tn in sorted(progress.notes[ex], key=int):
                    for n in progress.notes[ex][tn]:
                        print(f"    • {n}")
                print()

            elif cmd == ".progress":
                """Show overall progress across all exercises."""
                exercises = sorted(f.stem for f in EX_DIR.glob("*.sql"))
                total_tasks = 0
                total_done = 0
                total_errors = 0
                print()
                print("── Progress ────────────────────────────────────────")
                for ex in exercises:
                    try:
                        data = parse_exercise(EX_DIR / f"{ex}.sql")
                        tasks = data["tasks"]
                        n = len(tasks)
                        d = sum(1 for t in tasks if progress.is_completed(ex, t["num"]))
                        e = sum(
                            1
                            for t in tasks
                            if ex in progress.errors and t["num"] in progress.errors[ex]
                        )
                        total_tasks += n
                        total_done += d
                        total_errors += e
                        bar = "▓" * d + "░" * (n - d)
                        print(f"  {ex}  {bar}  {d}/{n}")
                    except Exception:
                        print(f"  {ex}  ? (parse error)")
                print(
                    f"\n  Total: {total_done}/{total_tasks} completed, {total_errors} with errors"
                )
                print()
            elif cmd == ".report":
                if not current_exercise:
                    print("No exercise loaded.")
                    continue
                _show_report(current_exercise, exercise_data)
                print()

            else:
                print(f"Unknown: {cmd}. Try .help")

        # ── SQL query ────────────────────────────────────────────
        else:
            # Support multi-line
            query = inp
            while not query.rstrip().endswith(";"):
                try:
                    line = session.prompt("...> ").strip()
                except EOFError:
                    break
                query += "\n" + line
            query = query.rstrip().rstrip(";")
            last_query = query

            try:
                cur.execute(query)
                rows = cur.fetchall()
                if cur.description:
                    headers = [d[0] for d in cur.description]
                    print(f"({len(rows)} row{'s' if len(rows)!=1 else ''})")
                    print(fmt_rows(rows, headers))
                else:
                    print(f"OK ({cur.rowcount})")
                    conn.commit()
            except Exception as e:
                print(f"Error: {e}")

    conn.close()


if __name__ == "__main__":
    repl()
