from datetime import date, timedelta

# Represents a single care activity (e.g. "Walk", "Feed", "Groom").
# Tracks what the task is, how long it takes, and whether it's been done.
class Task:
    def __init__(self, name: str, duration_minutes: int, category: str,
                 time: str = "00:00", frequency: str = None, due_date: str = None):
        """Initialize a Task with a name, duration, category, and scheduled time.

        frequency: optional recurrence — "daily" or "weekly"
        due_date:  optional date string "YYYY-MM-DD" when the task is due
        """
        self.name = name
        self.duration_minutes = duration_minutes
        self.category = category
        self.time = time           # scheduled time in "HH:MM" format
        self.frequency = frequency # "daily", "weekly", or None
        self.due_date = due_date   # "YYYY-MM-DD" or None
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
    def __init__(self, date: str):
        """Initialize an empty Plan for the given date (YYYY-MM-DD)."""
        self.date = date
        self.tasks: list[PetTask] = []    # tasks scheduled for this date
        self.skipped: list[PetTask] = []  # tasks skipped due to time conflicts
        self.total_duration = 0           # running total of minutes across all tasks
        self.reasoning = ""               # explanation of how the plan was built
        self.scheduler = Scheduler(self.tasks)  # shares the same list reference

    def add_task(self, pet_task: PetTask):
        """Add a PetTask to the plan and update the total duration."""
        self.tasks.append(pet_task)
        self.total_duration += pet_task.task.duration_minutes

    def get_summary(self) -> str:
        """Return a formatted string listing all tasks and the total time."""
        lines = [f"Plan for {self.date}:"]
        for pt in self.tasks:
            # checkmark = done, circle = still to do
            status = "\u2713" if pt.task.is_completed else "\u25cb"
            lines.append(
                f"  {status} [{pt.task.category}] {pt.pet.name}: {pt.task.name} "
                f"({pt.task.duration_minutes} min, priority {pt.priority})"
            )
        lines.append(f"Total time: {self.total_duration} min")
        return "\n".join(lines)

    def explain_reasoning(self) -> str:
        """Return the reasoning string explaining how this plan was built."""
        return self.reasoning


def _time_to_minutes(time_str: str) -> int:
    """Convert a 'HH:MM' string to total minutes since midnight."""
    h, m = time_str.split(":")
    return int(h) * 60 + int(m)


def _conflicts(candidate, scheduled: list) -> bool:
    """Return True if candidate's time window overlaps any already-scheduled task."""
    c_start = _time_to_minutes(candidate.task.time)
    c_end = c_start + candidate.task.duration_minutes
    for pt in scheduled:
        s_start = _time_to_minutes(pt.task.time)
        s_end = s_start + pt.task.duration_minutes
        if c_start < s_end and c_end > s_start:
            return True
    return False


# Utility class for sorting and filtering a list of PetTasks.
class Scheduler:
    def __init__(self, pet_tasks: list):
        """Initialize with a list of PetTask objects (e.g. from plan.tasks)."""
        self.pet_tasks = pet_tasks

    def sort_by_time(self) -> list:
        """Return tasks sorted chronologically by their scheduled time (HH:MM)."""
        return sorted(self.pet_tasks, key=lambda pt: pt.task.time)

    def filter_tasks(self, is_completed: bool = None, pet_name: str = None) -> list:
        """Return tasks filtered by completion status and/or pet name."""
        result = self.pet_tasks
        if is_completed is not None:
            result = [pt for pt in result if pt.task.is_completed == is_completed]
        if pet_name is not None:
            result = [pt for pt in result if pt.pet.name == pet_name]
        return result

    def check_conflicts(self) -> list:
        """Return a list of warning strings for any overlapping task time windows.

        Compares every pair of tasks in the scheduler. If two tasks overlap,
        a human-readable warning is appended — no exception is raised.
        Returns an empty list when there are no conflicts.
        """
        warnings = []
        tasks = list(self.pet_tasks)
        for i, a in enumerate(tasks):
            for b in tasks[i + 1:]:
                a_start = _time_to_minutes(a.task.time)
                a_end   = a_start + a.task.duration_minutes
                b_start = _time_to_minutes(b.task.time)
                b_end   = b_start + b.task.duration_minutes
                if a_start < b_end and a_end > b_start:
                    warnings.append(
                        f"WARNING: '{a.pet.name}: {a.task.name}' "
                        f"({a.task.time}, {a.task.duration_minutes} min) "
                        f"overlaps with '{b.pet.name}: {b.task.name}' "
                        f"({b.task.time}, {b.task.duration_minutes} min)"
                    )
        return warnings

    def mark_task_complete(self, pet_task) -> "Task | None":
        """Mark a PetTask's task complete and, for recurring tasks, return a new Task
        scheduled for the next occurrence.

        - "daily"  → next due date is today + 1 day   (timedelta(days=1))
        - "weekly" → next due date is today + 7 days  (timedelta(days=7))

        Returns the new Task instance if one was created, otherwise None.
        """
        task = pet_task.task
        task.complete()

        if task.frequency not in ("daily", "weekly"):
            return None

        # Calculate the next due date using timedelta
        delta = timedelta(days=1) if task.frequency == "daily" else timedelta(days=7)
        next_due = date.today() + delta

        return Task(
            name=task.name,
            duration_minutes=task.duration_minutes,
            category=task.category,
            time=task.time,
            frequency=task.frequency,
            due_date=str(next_due),   # "YYYY-MM-DD"
        )


# The pet owner who manages multiple pets and generates daily care plans.
class PetOwner:
    def __init__(self, name: str):
        """Initialize a PetOwner with a name."""
        self.name = name
        self.plans: dict[str, Plan] = {}  # generated plans by date
        self.pets: list[Pet] = []         # all pets owned

    def add_pet(self, pet: Pet):
        """Register a pet under this owner."""
        self.pets.append(pet)

    def generate_plan(self, date: str) -> Plan:
        """Build and store a care plan for the given date.

        Tasks are sorted by priority (1 = highest). Ties are broken by scheduled
        time -- the earlier task wins. A task is skipped only if its time window
        conflicts with an already-scheduled task.
        """
        plan = Plan(date=date)

        # Gather every PetTask from every pet into one flat list
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.pet_tasks)

        # Sort by priority ascending, then by scheduled time for ties
        all_tasks.sort(key=lambda pt: (pt.priority, pt.task.time))

        for pt in all_tasks:
            if _conflicts(pt, plan.tasks):
                plan.skipped.append(pt)
            else:
                plan.add_task(pt)

        # Record why certain tasks were skipped
        if plan.skipped:
            skipped_names = ", ".join(
                f"{pt.pet.name}'s {pt.task.name}" for pt in plan.skipped
            )
            plan.reasoning = (
                f"Tasks were added in priority order. "
                f"Skipped due to time conflicts: {skipped_names}."
            )
        else:
            plan.reasoning = "All tasks were scheduled with no time conflicts."

        self.plans[date] = plan
        return plan
