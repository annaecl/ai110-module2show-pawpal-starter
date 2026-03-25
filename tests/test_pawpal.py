import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, PetOwner


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


# Test 3: generate_plan() schedules tasks sorted by priority, then by duration for ties
def test_tasks_sorted_by_priority_and_duration():
    owner = PetOwner(name="Jordan")
    owner.set_available_time("Monday", 120)

    pet = Pet(name="Mochi", species="dog", breed="Shiba")
    # Added in scrambled order to ensure sorting is actually happening
    pet.add_task(Task("Grooming",     duration_minutes=15, category="grooming"),  priority=3)
    pet.add_task(Task("Morning walk", duration_minutes=20, category="exercise"),  priority=1)
    pet.add_task(Task("Medication",   duration_minutes=5,  category="health"),    priority=2)
    # Two tasks share priority=1 — the shorter one (10 min) should come before the longer one (20 min)
    pet.add_task(Task("Quick check",  duration_minutes=10, category="health"),    priority=1)
    owner.add_pet(pet)

    plan = owner.generate_plan("Monday")
    actual = [(pt.priority, pt.task.duration_minutes) for pt in plan.tasks]
    expected = [
        (1, 10),   # Quick check  — priority 1, 10 min
        (1, 20),   # Morning walk — priority 1, 20 min
        (2, 5),    # Medication   — priority 2,  5 min
        (3, 15),   # Grooming     — priority 3, 15 min
    ]
    assert actual == expected, f"Expected {expected}, got {actual}"
