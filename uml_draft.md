classDiagram
    class PetOwner {
        +String name
        +Dict~String,int~ available_minutes_per_day
        +Dict~String,Plan~ weekly_plan
        +List~Pet~ pets
        +add_pet(pet: Pet)
        +generate_plan(day: String) Plan
    }

    class Pet {
        +String name
        +String species
        +String breed
        +List~PetTask~ pet_tasks
        +add_task(task: Task, priority: int)
        +get_tasks() List~PetTask~
    }

    class Task {
        +String name
        +int duration_minutes
        +String category
        +bool is_completed
        +complete()
    }

    class PetTask {
        +Pet pet
        +Task task
        +int priority
    }

    class Plan {
        +String date
        +String day_of_week
        +List~PetTask~ tasks
        +int total_duration
        +String reasoning
        +add_task(pet_task: PetTask)
        +get_summary() String
        +explain_reasoning() String
    }

    PetOwner "1" --> "1..*" Pet : owns
    PetOwner "1" --> "1" Plan : generates
    Pet "1" --> "1..*" PetTask : has
    PetTask --> "1" Task : references
    Plan "1" o-- "0..*" PetTask : includes
