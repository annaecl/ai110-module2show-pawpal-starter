# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Demo 
<a href="/demo.png" target="_blank"><img src='/demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

## Features

- **Priority-based plan generation** — `PetOwner.generate_plan()` schedules tasks in priority order (1 = highest), using scheduled time as a tiebreaker when priorities are equal.

- **Chronological sorting** — `Scheduler.sort_by_time()` returns tasks sorted by their `HH:MM` scheduled time using Python's built-in `sorted()` with a key function.

- **Conflict detection** — `Scheduler.check_conflicts()` runs an O(n²) pairwise comparison of every task's time window (`start` to `start + duration`) and reports human-readable warnings for any overlapping pairs.

- **Conflict-aware scheduling** — `generate_plan()` uses `_conflicts()` to skip any task whose time window overlaps an already-scheduled task, logging skipped tasks in `Plan.reasoning`.

- **Daily and weekly recurrence** — `Scheduler.mark_task_complete()` marks a task done and, for `frequency="daily"` or `"weekly"` tasks, automatically creates a new `Task` with the next due date calculated via `timedelta`.

- **Task filtering** — `Scheduler.filter_tasks()` lets you query tasks by completion status, by pet name, or both simultaneously.

- **Multi-pet support** — A `PetOwner` manages multiple `Pet` objects, each with their own prioritized `PetTask` list, all merged into a single daily plan.

- **Plan summary with status indicators** — `Plan.get_summary()` renders each task with a ✓ (done) or ○ (pending) marker, category label, duration, and priority.

- **Explainable reasoning** — `Plan.explain_reasoning()` returns a plain-English string describing which tasks were skipped and why.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Testing PawPal+

### Running the tests

```bash
python -m pytest
```

### What the tests cover

| Test | What it verifies |
|------|-----------------|
| `test_task_completion` | `Task.complete()` flips `is_completed` from `False` to `True` |
| `test_task_addition_increases_count` | `Pet.add_task()` correctly appends a task to the pet's task list |
| `test_sort_by_time_returns_chronological_order` | `Scheduler.sort_by_time()` returns tasks sorted earliest → latest regardless of insertion order |
| `test_daily_recurring_task_schedules_next_occurrence` | Completing a `"daily"` task marks it done and auto-generates a new occurrence due tomorrow |
| `test_check_conflicts_detects_duplicate_times` | `Scheduler.check_conflicts()` flags two tasks that overlap at the same start time |

> **Note:** One test (`test_tasks_sorted_by_priority_and_duration`) is currently commented out pending a refinement to tie-breaking logic.

### Confidence Level

**3 / 5 stars**

The core behaviors — task completion, task addition, chronological sorting, conflict detection, and daily recurrence — are all verified and passing. Confidence is held back by the commented-out priority tie-breaking test and the lack of coverage for edge cases such as overlapping (but not identical) time windows, weekly recurrence, and the full `generate_plan` pipeline end-to-end.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

