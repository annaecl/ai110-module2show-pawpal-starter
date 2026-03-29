import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Task, Pet, PetTask, PetOwner, Scheduler


# Test 1: mark_complete() changes the task's status
def test_task_completion():
    task = Task(name="Morning walk", duration_minutes=20, category="exercise")
    assert task.is_completed is False  # starts as not done
    task.complete()
    assert task.is_completed is True   # should now be marked done


# Test 2: adding a task to a Pet increases its task count
def test_task_addition_increases_count():
    pet = Pet(name="Mochi", species="dog", breed="Shiba")
    task = Task(name="Feed breakfast", duration_minutes=5, category="feeding")

    assert len(pet.pet_tasks) == 0
    pet.add_task(task, priority=1)
    assert len(pet.pet_tasks) == 1


# # Test 3: generate_plan() schedules tasks sorted by priority, then by duration for ties
# def test_tasks_sorted_by_priority_and_duration():
#     owner = PetOwner(name="Jordan")
#     owner.set_available_time("Monday", 120)

#     pet = Pet(name="Mochi", species="dog", breed="Shiba")
#     # Added in scrambled order to ensure sorting is actually happening
#     pet.add_task(Task("Grooming",     duration_minutes=15, category="grooming"),  priority=3)
#     pet.add_task(Task("Morning walk", duration_minutes=20, category="exercise"),  priority=1)
#     pet.add_task(Task("Medication",   duration_minutes=5,  category="health"),    priority=2)
#     # Two tasks share priority=1 — the shorter one (10 min) should come before the longer one (20 min)
#     pet.add_task(Task("Quick check",  duration_minutes=10, category="health"),    priority=1)
#     owner.add_pet(pet)

#     plan = owner.generate_plan("Monday")
#     actual = [(pt.priority, pt.task.duration_minutes) for pt in plan.tasks]
#     expected = [
#         (1, 10),   # Quick check  — priority 1, 10 min
#         (1, 20),   # Morning walk — priority 1, 20 min
#         (2, 5),    # Medication   — priority 2,  5 min
#         (3, 15),   # Grooming     — priority 3, 15 min
#     ]
#     assert actual == expected, f"Expected {expected}, got {actual}"


# Test 4: sort_by_time() returns tasks in chronological order
def test_sort_by_time_returns_chronological_order():
    pet = Pet(name="Mochi", species="dog", breed="Shiba")
    # Add tasks in scrambled time order
    pet.add_task(Task("Afternoon walk", duration_minutes=20, category="exercise", time="14:00"), priority=1)
    pet.add_task(Task("Evening meds",   duration_minutes=5,  category="health",   time="19:30"), priority=1)
    pet.add_task(Task("Morning feed",   duration_minutes=10, category="feeding",  time="07:00"), priority=1)

    scheduler = Scheduler(pet.pet_tasks)
    sorted_tasks = scheduler.sort_by_time()
    actual_times = [pt.task.time for pt in sorted_tasks]

    assert actual_times == ["07:00", "14:00", "19:30"], f"Expected chronological order, got {actual_times}"


# Test 5: marking a daily task complete returns a new task due tomorrow
def test_daily_recurring_task_schedules_next_occurrence():
    pet = Pet(name="Mochi", species="dog", breed="Shiba")
    daily_task = Task("Morning feed", duration_minutes=10, category="feeding",
                      time="08:00", frequency="daily")
    pet.add_task(daily_task, priority=1)
    pet_task = pet.pet_tasks[0]

    scheduler = Scheduler(pet.pet_tasks)
    next_task = scheduler.mark_task_complete(pet_task)

    # Original task should now be marked done
    assert pet_task.task.is_completed is True

    # A new task should be returned for tomorrow
    assert next_task is not None
    assert next_task.is_completed is False
    assert next_task.frequency == "daily"
    expected_due = str(date.today() + timedelta(days=1))
    assert next_task.due_date == expected_due, f"Expected {expected_due}, got {next_task.due_date}"


# Test 6: check_conflicts() flags two tasks scheduled at the same time
def test_check_conflicts_detects_duplicate_times():
    pet = Pet(name="Mochi", species="dog", breed="Shiba")
    # Both tasks start at 09:00 — clear overlap
    pet.add_task(Task("Morning walk", duration_minutes=30, category="exercise", time="09:00"), priority=1)
    pet.add_task(Task("Breakfast",    duration_minutes=10, category="feeding",  time="09:00"), priority=2)

    scheduler = Scheduler(pet.pet_tasks)
    warnings = scheduler.check_conflicts()

    assert len(warnings) == 1, f"Expected 1 conflict warning, got {len(warnings)}"
    assert "overlaps with" in warnings[0]
