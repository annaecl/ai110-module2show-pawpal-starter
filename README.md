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

## Smarter Scheduling

PawPal+ goes beyond a simple task list with several scheduling improvements:

- **Priority-based ordering** — tasks are sorted by priority (1 = most important) so critical care always gets scheduled first. Ties are broken by the task's scheduled time.
- **Conflict detection** — before adding any task to the plan, the scheduler checks whether its time window overlaps with an already-scheduled task. Conflicting tasks are moved to a `skipped` list and reported in the plan's reasoning.
- **Recurring tasks** — tasks can be marked `"daily"` or `"weekly"`. Completing a recurring task automatically generates the next occurrence with the correct due date (`today + 1 day` or `today + 7 days`).
- **Explained reasoning** — every generated plan includes a human-readable summary of why certain tasks were chosen and which (if any) were skipped due to time conflicts.
- **Flexible filtering** — the `Scheduler` utility can filter tasks by completion status or by pet name, making it easy to show only what's left to do or focus on one pet at a time.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

