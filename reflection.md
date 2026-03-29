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
I was trying to figure out how to make the relationship between Task and Pet more flexible given that each task may have a priority that is specific to a certain pet (for example, going on a walk may be higher priority for a dog than for a cat.) Claude Code suggested that I create a mediating class, called Pet Task, that would link a specific task to a specific pet, and then create a priority given this context. I incorporated this change into my UML diagram. 

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
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
