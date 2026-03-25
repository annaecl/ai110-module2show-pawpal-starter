from pawpal_system import Task, Pet, PetOwner

# Create owner
owner = PetOwner("Anna")

# Create two pets
buddy = Pet("Buddy", "Dog", "Golden Retriever")
whiskers = Pet("Whiskers", "Cat", "Siamese")

# Register pets with owner
owner.add_pet(buddy)
owner.add_pet(whiskers)

# Create tasks with different durations
morning_walk = Task("Morning Walk", 30, "Exercise")
feeding = Task("Feeding", 10, "Nutrition")
grooming = Task("Grooming", 20, "Hygiene")
playtime = Task("Playtime", 15, "Exercise")

# Add tasks to pets with priority levels
buddy.add_task(morning_walk, priority=1)
buddy.add_task(feeding, priority=2)
buddy.add_task(grooming, priority=3)

whiskers.add_task(feeding, priority=1)
whiskers.add_task(playtime, priority=2)

# Generate and print Today's Schedule
plan = owner.generate_plan("Wednesday")
print(plan.get_summary())
print()
print(plan.explain_reasoning())
