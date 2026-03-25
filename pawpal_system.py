# Represents a single care activity (e.g. "Walk", "Feed", "Groom").
# Tracks what the task is, how long it takes, and whether it's been done.
class Task:
    def __init__(self, name: str, duration_minutes: int, category: str):
        """Initialize a Task with a name, duration, and category."""
        self.name = name
        self.duration_minutes = duration_minutes
        self.category = category
        self.is_completed = False  # starts as not done

    def complete(self):
        """Mark this task as completed."""
        self.is_completed = True


# Links a Task to a specific Pet with a priority number.
# Priority 1 = most important; higher numbers = lower importance.
# This lets the same Task type be assigned to different pets with different urgency.
class PetTask:
    def __init__(self, pet, task: Task, priority: int):
        """Initialize a PetTask linking a pet to a task with a given priority."""
        self.pet = pet        # which pet this task belongs to
        self.task = task      # the task details (name, duration, category)
        self.priority = priority


# Represents a pet with its own list of care tasks.
class Pet:
    def __init__(self, name: str, species: str, breed: str):
        """Initialize a Pet with a name, species, and breed."""
        self.name = name
        self.species = species
        self.breed = breed
        self.pet_tasks: list[PetTask] = []  # all tasks assigned to this pet

    def add_task(self, task: Task, priority: int):
        """Wrap the task in a PetTask and add it to this pet's task list."""
        self.pet_tasks.append(PetTask(self, task, priority))

    def get_tasks(self) -> list[PetTask]:
        """Return all PetTasks assigned to this pet."""
        return self.pet_tasks


# A daily schedule of PetTasks for a specific date.
# Tracks which tasks are planned, total time required, and why tasks were chosen.
class Plan:
    def __init__(self, day_of_week: str):
        """Initialize an empty Plan for the given day of the week."""
        self.day_of_week = day_of_week
        self.tasks: list[PetTask] = []    # tasks scheduled for this day
        self.skipped: list[PetTask] = []  # tasks that didn't fit within available time
        self.total_duration = 0           # running total of minutes across all tasks
        self.reasoning = ""               # explanation of how the plan was built

    def add_task(self, pet_task: PetTask):
        """Add a PetTask to the plan and update the total duration."""
        self.tasks.append(pet_task)
        self.total_duration += pet_task.task.duration_minutes

    def get_summary(self) -> str:
        """Return a formatted string listing all tasks and the total time."""
        lines = [f"Plan for {self.day_of_week}:"]
        for pt in self.tasks:
            # ✓ = done, ○ = still to do
            status = "✓" if pt.task.is_completed else "○"
            lines.append(
                f"  {status} [{pt.task.category}] {pt.pet.name}: {pt.task.name} "
                f"({pt.task.duration_minutes} min, priority {pt.priority})"
            )
        lines.append(f"Total time: {self.total_duration} min")
        return "\n".join(lines)

    def explain_reasoning(self) -> str:
        """Return the reasoning string explaining how this plan was built."""
        # Return the explanation set when the plan was generated
        return self.reasoning


# The pet owner who manages multiple pets and generates daily care plans.
class PetOwner:
    def __init__(self, name: str):
        """Initialize a PetOwner with a name and default 60-minute daily availability."""
        self.name = name
        self.available_minutes_per_day: dict[str, int] = {
            "Monday": 60, "Tuesday": 60, "Wednesday": 60,
            "Thursday": 60, "Friday": 60, "Saturday": 60, "Sunday": 60
        }
        self.weekly_plan: dict[str, Plan] = {}               # generated plans by day
        self.pets: list[Pet] = []                            # all pets owned

    def set_available_time(self, day: str, minutes: int):
        """Set the number of available care minutes for a specific day."""
        self.available_minutes_per_day[day] = minutes

    def add_pet(self, pet: Pet):
        """Register a pet under this owner."""
        self.pets.append(pet)

    def generate_plan(self, day: str) -> Plan:
        """Build and store a priority-ordered care plan for the given day, skipping tasks that don't fit."""
        plan = Plan(day_of_week=day)

        # Look up how many minutes the owner has free on this day (default 0)
        available = self.available_minutes_per_day.get(day, 0)

        # Gather every PetTask from every pet into one flat list
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())

        # Sort by priority ascending, then by duration ascending for ties
        all_tasks.sort(key=lambda pt: (pt.priority, pt.task.duration_minutes))

        for pt in all_tasks:
            if pt.task.duration_minutes <= available:
                # Task fits — add it and subtract its time from what's left
                plan.add_task(pt)
                available -= pt.task.duration_minutes
            else:
                # Not enough time remaining — record it as skipped
                plan.skipped.append(pt)

        # Record why certain tasks were included or left out
        if plan.skipped:
            skipped_names = ", ".join(
                f"{pt.pet.name}'s {pt.task.name}" for pt in plan.skipped
            )
            plan.reasoning = (
                f"Tasks were added in priority order. "
                f"Skipped due to time constraints: {skipped_names}."
            )
        else:
            plan.reasoning = "All tasks fit within the available time for the day."


        # Save the plan so it can be retrieved later without regenerating
        self.weekly_plan[day] = plan
        return plan
