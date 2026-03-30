# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

### Three core actions: 
1. Add a pet, attached to specific tasks
2. Generate a daily plan 
3. Input user information, such as constraints 

I think I probably will need four main classes: 
- Care Task
    - Attributes: duration, priority, name, description
- Pet
    - Attributes: name, age, type, list of required tasks 
- Pet Caretaker
    - Attributes: first name, last name, age, list of pets, weekly plan?
- Plan 
    - Attributes: date, lists of tasks 

- What classes did you include, and what responsibilities did you assign to each?

- Care Task
    - Responsibilities: 
- Pet
    - Responsibilities: have an updated list of necessary tasks? 
- Pet Caretaker
    - Responsabilities: generate new plans
- Plan 
    - Responsabilities: 

**b. Design changes**

- Did your design change during implementation? Yes!
- If yes, describe at least one change and why you made it.
I was trying to figure out how to make the relationship between Task and Pet more flexible given that each task may have a priority that is specific to a certain pet (for example, going on a walk may be higher priority for a dog than for a cat.) Claude Code suggested that I create a mediating class, called Pet Task, that would link a specific task to a specific pet, and then create a priority given this context. I incorporated this change into my UML diagram. I also added a Scheduler class to handle some of the more complicated components of the plan generation process, such as resolving conficts. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
We allow the owner to indicate a time for the task, how long the task will take, and the relative priority of the task. However, there are some constraints: two tasks can't be scheduled for the same time, so we prioritize: a. tasks that are high priority, and b. tasks that are scheduled first. 

- How did you decide which constraints mattered most?
Resolving conflicts was probably the most important constraint to consider, given that failing to address this potential issue would result in nonsensical plans. However, I did not factor in the amount of free time of the owner into the plans, as this would add unnecessary complexity. I will discuss this below. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler does not consider the amount of free time the owner has every particular day. 
- Why is that tradeoff reasonable for this scenario?
Initially, I designed the program to be a weekly schedule, so it made sense for the owner to indicate how much free time she expected to have each day of the week (assuming she had a regular schedule). However, as the program evolved, I decided to switch it up and allow the owner to generate plans for specific dates instead. This made it less reasonable to expect the owner to know how much free time she would have at said future date, and it seemed more beneficial to have a full plan organized based on priority. That way the owner could have access to a full plan but decide what to actually complete herself. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
In particular during the planning phase, I used AI agents to help design the UML diagram; I would give the AI feedback on the necessary specifications or questions I had about the functionality of the design. It was also very helpful for refactoring quickly: there were several moments where I found I needed to take the program in a slightly different direction, which would require several small changes throughout the application. The AI was good at identifying and correcting all these minor components. 

- What kinds of prompts or questions were most helpful
I often asked the AI to walk me through what it had changed so that I could verify that the logic was sound. This way I could more easily skim through the code it rewrote, since I already had the context of what it had changed and what it was supposed to do (that way I could also identify potential gaps in its logic).

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
I was discussing with the AI whether or not I should better link the Plan and Scheduler classes. It said to leave them separate, in case I wanted to use the Scheduler in other contexts besides plans. But this didn't make sense for this program, since the scheduler is really only helpful for generating plans and resolving conflicts. 

- How did you evaluate or verify what the AI suggested?
I evaluated this by studying the UML diagram, and considering what relationship between Plans and the Scheduler would make sense in practice. Since the scope of this project is small, I decided to make it so that each Plan has a Scheduler. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test? & Why were these tests important?
1. Task completion and task addition verify the foundational data model to make sure that the rest of the program will work. 
2. Chronological sorting is critical for producing a readable, sensible daily plan. Without it, a user could see evening tasks listed before morning ones, and this would not be intuitive for the user. 
3. Recurring tasks are central to pet care (daily feeding, medication, walks), so ensuring the next occurrence is scheduled correctly prevents tasks from being silently dropped.
4. Conflict detection is arguably the most important because two tasks at the same time produces a nonsensical plan and creates confusion. This test ensures the scheduler catches that before it reaches the user.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am somewhat confident, although there are some edge cases I would definitely want to check. 
- What edge cases would you test next if you had more time?
I want to check what happens when two tasks are scheduled for the same time with the same priority. I also want to verify that the scheduler functions properly with many pets and tasks. Also, what would happen if tasks were scheduled for more minutes than there are in a day?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with the UI, because I think it performs the basic program functions very cleanly and it is pretty intuitive for the user. I think I also covered some basic edge cases that prevent at least some fundamental errors. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would like to refine the UML structure and clean up some duplication I think might exist in the pawpal_system.py file. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
It takes a lot of iteration, and careful planning is very important. Also, understanding the full scope of the specification is critical: I would have planned things a little differently if I had looked ahead farther in the project (ex: to prepare for sorting). 