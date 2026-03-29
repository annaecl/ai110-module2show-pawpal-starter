from pawpal_system import Task, Pet, PetOwner

# Create owner
owner = PetOwner("Anna")

# Create two pets
buddy = Pet("Buddy", "Dog", "Golden Retriever")
whiskers = Pet("Whiskers", "Cat", "Siamese")

# Register pets with owner
owner.add_pet(buddy)
owner.add_pet(whiskers)

# Create tasks with different durations and scheduled times (intentionally out of order)
# morning_walk and playtime are recurring so they auto-reschedule when completed
morning_walk = Task("Morning Walk", 30, "Exercise", time="08:00", frequency="daily")
feeding      = Task("Feeding",      10, "Nutrition", time="14:00", frequency="daily")
grooming     = Task("Grooming",     20, "Hygiene",   time="09:30", frequency="weekly")
playtime     = Task("Playtime",     15, "Exercise",  time="11:00", frequency="daily")

# Add tasks to pets with priority levels
buddy.add_task(morning_walk, priority=1)
buddy.add_task(feeding, priority=2)
buddy.add_task(grooming, priority=3)

whiskers.add_task(feeding, priority=1)
whiskers.add_task(playtime, priority=2)

plan = owner.generate_plan("2026-03-29")
print(plan.get_summary())
print()
print(plan.explain_reasoning())

print("\n--- Sorted by Time ---")
for pt in plan.scheduler.sort_by_time():
    print(f"  {pt.task.time}  {pt.pet.name}: {pt.task.name}")

# Mark tasks complete via Scheduler — recurring tasks automatically get a next occurrence
buddy_walk_pt = next(pt for pt in plan.tasks if pt.task.name == "Morning Walk")
next_task = plan.scheduler.mark_task_complete(buddy_walk_pt)
if next_task:
    print(f"\nRecurring task '{next_task.name}' rescheduled → next due: {next_task.due_date}")

print("\n--- Completed Tasks ---")
for pt in plan.scheduler.filter_tasks(is_completed=True):
    print(f"  ✓ {pt.pet.name}: {pt.task.name}")

print("\n--- Buddy's Tasks ---")
for pt in plan.scheduler.filter_tasks(pet_name="Buddy"):
    status = "✓" if pt.task.is_completed else "○"
    print(f"  {status} {pt.task.name}")

print("\n--- Conflict Detection ---")
warnings = plan.scheduler.check_conflicts()
if warnings:
    for w in warnings:
        print(w)
else:
    print("No conflicts detected.")
