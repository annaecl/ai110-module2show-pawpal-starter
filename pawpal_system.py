class Task:
    def __init__(self, name: str, duration_minutes: int, category: str):
        self.name = name
        self.duration_minutes = duration_minutes
        self.category = category
        self.is_completed = False

    def complete(self):
        self.is_completed = True


class PetTask:
    def __init__(self, pet, task: Task, priority: int):
        self.pet = pet
        self.task = task
        self.priority = priority


class Pet:
    def __init__(self, name: str, species: str, breed: str):
        self.name = name
        self.species = species
        self.breed = breed
        self.pet_tasks: list[PetTask] = []

    def add_task(self, task: Task, priority: int):
        pass

    def get_tasks(self) -> list[PetTask]:
        pass


class Plan:
    def __init__(self, date: str, day_of_week: str):
        self.date = date
        self.day_of_week = day_of_week
        self.tasks: list[PetTask] = []
        self.total_duration = 0
        self.reasoning = ""

    def add_task(self, pet_task: PetTask):
        pass

    def get_summary(self) -> str:
        pass

    def explain_reasoning(self) -> str:
        pass


class PetOwner:
    def __init__(self, name: str):
        self.name = name
        self.available_minutes_per_day: dict[str, int] = {}
        self.weekly_plan: dict[str, Plan] = {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def generate_plan(self, day: str) -> Plan:
        pass
