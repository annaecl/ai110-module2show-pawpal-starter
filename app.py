import streamlit as st
from datetime import date
from pawpal_system import Task, Pet, PetOwner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant that builds a priority-based daily schedule.")

# ── Initialize session state vaults ──────────────────────────────────────────
if "owner_name" not in st.session_state:
    st.session_state.owner_name = ""

if "availability" not in st.session_state:
    st.session_state.availability = {}  # {date_string: minutes}

if "pets" not in st.session_state:
    st.session_state.pets = []   # list of dicts: {name, species, breed}

if "tasks" not in st.session_state:
    st.session_state.tasks = []  # list of dicts: {pet_name, name, duration_minutes, priority, category, time, frequency}

if "next_tasks" not in st.session_state:
    st.session_state.next_tasks = {}  # {task_key: next Task} — next occurrence after completing a recurring task

if "selected_date" not in st.session_state:
    st.session_state.selected_date = date.today()

# ── Step 1: Owner ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("Step 1 — Owner")

col_name, col_btn = st.columns([3, 1])
with col_name:
    owner_input = st.text_input("Owner name", value=st.session_state.owner_name)
with col_btn:
    st.write("")  # spacer to align button with input
    if st.button("Save owner"):
        new_name = owner_input.strip()
        if new_name != st.session_state.owner_name:
            # Owner changed — reset everything tied to the previous owner
            st.session_state.owner_name = new_name
            st.session_state.availability = {}
            st.session_state.pets = []
            st.session_state.tasks = []
            if "plan" in st.session_state:
                del st.session_state.plan

if st.session_state.owner_name:
    st.success(f"Owner: **{st.session_state.owner_name}**")
else:
    st.info("Enter an owner name and click Save owner.")


# ── Step 2: Pets ──────────────────────────────────────────────────────────────
st.divider()
st.subheader("Step 2 — Pets")

col_pet, col_species, col_breed, col_add = st.columns([2, 1, 2, 1])
with col_pet:
    pet_name_input = st.text_input("Pet name")
with col_species:
    species_input = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])
with col_breed:
    breed_input = st.text_input("Breed", value="Mixed")
with col_add:
    st.write("")  # spacer
    if st.button("Add pet"):
        name = pet_name_input.strip()
        existing_names = [p["name"] for p in st.session_state.pets]
        if not name:
            st.warning("Enter a pet name first.")
        elif name in existing_names:
            st.warning(f"{name} is already added.")
        else:
            st.session_state.pets.append({
                "name": name,
                "species": species_input,
                "breed": breed_input.strip() or "Mixed",
            })

if st.session_state.pets:
    st.write("Your pets:")
    for i, pet in enumerate(st.session_state.pets):
        col_info, col_remove = st.columns([5, 1])
        with col_info:
            st.markdown(f"- **{pet['name']}** — {pet['species']}, {pet['breed']}")
        with col_remove:
            if st.button("Remove", key=f"remove_pet_{i}"):
                st.session_state.tasks = [
                    t for t in st.session_state.tasks if t["pet_name"] != pet["name"]
                ]
                st.session_state.pets.pop(i)
                st.rerun()
else:
    st.info("No pets added yet.")

# ── Step 3: Tasks ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("Step 3 — Tasks")

if not st.session_state.pets:
    st.info("Add at least one pet above before adding tasks.")
else:
    pet_names = [p["name"] for p in st.session_state.pets]

    col1, col2 = st.columns(2)
    with col1:
        task_pet = st.selectbox("For which pet?", pet_names)
        task_name = st.text_input("Task name", value="Morning walk")
    with col2:
        task_priority = st.selectbox("Priority", ["high", "medium", "low"])
        task_category = st.selectbox("Category", ["Exercise", "Nutrition", "Hygiene", "Health", "Play"])

    col_dur, col_time, col_freq = st.columns(3)
    with col_dur:
        task_duration = st.slider("Duration (minutes)", min_value=5, max_value=120, value=20, step=5)
    with col_time:
        task_time = st.time_input("Scheduled time", value=None, help="When this task should happen")
    with col_freq:
        task_frequency = st.selectbox("Frequency", ["none", "daily", "weekly"],
                                      help="Recurring tasks auto-reschedule when marked complete")

    if st.button("Add task"):
        time_str = task_time.strftime("%H:%M") if task_time else "00:00"
        st.session_state.tasks.append({
            "pet_name": task_pet,
            "name": task_name,
            "duration_minutes": task_duration,
            "priority": task_priority,
            "category": task_category,
            "time": time_str,
            "frequency": task_frequency if task_frequency != "none" else None,
        })

    if st.session_state.tasks:
        st.write("Current tasks:")
        for i, t in enumerate(st.session_state.tasks):
            col_info, col_remove = st.columns([5, 1])
            with col_info:
                freq_label = f", {t['frequency']}" if t.get("frequency") else ""
                st.markdown(
                    f"- **{t['name']}** for {t['pet_name']} — "
                    f"{t.get('time', '00:00')} | {t['duration_minutes']} min, {t['priority']} priority, {t['category']}{freq_label}"
                )
            with col_remove:
                if st.button("Remove", key=f"remove_task_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()
    else:
        st.info("No tasks yet.")

# ── Step 4: Generate Schedule ─────────────────────────────────────────────────
st.divider()
st.subheader("Step 4 — Generate Schedule")

selected_date = st.date_input("Date to generate plan for", value=st.session_state.selected_date)

# When the date changes, remove one-off tasks and clear the current plan
if selected_date != st.session_state.selected_date:
    st.session_state.selected_date = selected_date
    st.session_state.tasks = [t for t in st.session_state.tasks if t.get("frequency")]
    st.session_state.next_tasks = {}
    if "plan" in st.session_state:
        del st.session_state.plan

date_str = selected_date.strftime("%Y-%m-%d")

if st.button("Generate schedule", type="primary"):
    if not st.session_state.owner_name:
        st.warning("Save an owner name in Step 1 first.")
    elif not st.session_state.pets:
        st.warning("Add at least one pet in Step 2 first.")
    elif not st.session_state.tasks:
        st.warning("Add at least one task in Step 3 first.")
    else:
        priority_map = {"high": 1, "medium": 2, "low": 3}

        owner = PetOwner(name=st.session_state.owner_name)

        # Build a Pet object for each saved pet (with breed)
        pet_objects = {}
        for p in st.session_state.pets:
            pet_obj = Pet(name=p["name"], species=p["species"], breed=p["breed"])
            owner.add_pet(pet_obj)
            pet_objects[p["name"]] = pet_obj

        # Add each task to its pet
        for t in st.session_state.tasks:
            task = Task(
                name=t["name"],
                duration_minutes=t["duration_minutes"],
                category=t["category"],
                time=t.get("time", "00:00"),
                frequency=t.get("frequency"),
            )
            pet_objects[t["pet_name"]].add_task(task, priority=priority_map[t["priority"]])

        # Generate and store the plan; clear any stale next-task info
        st.session_state.plan = owner.generate_plan(date_str)
        st.session_state.next_tasks = {}

# ── Display Plan ──────────────────────────────────────────────────────────────
if "plan" in st.session_state:
    plan = st.session_state.plan
    st.divider()
    st.subheader(f"Schedule — {plan.date}")

    if plan.tasks:
        for i, pt in enumerate(plan.scheduler.sort_by_time()):
            priority_label = {1: "high", 2: "medium", 3: "low"}.get(pt.priority, str(pt.priority))
            task_key = f"{pt.pet.name}_{pt.task.name}_{pt.task.time}"
            freq_badge = f" 🔁 {pt.task.frequency}" if pt.task.frequency else ""

            col_task, col_btn = st.columns([5, 1])
            with col_task:
                if pt.task.is_completed:
                    st.markdown(
                        f"✅ ~~**{pt.task.time}** &nbsp;|&nbsp; **{pt.task.name}** for {pt.pet.name}~~ &nbsp;|&nbsp; "
                        f"{pt.task.duration_minutes} min &nbsp;|&nbsp; "
                        f"Priority: {priority_label} &nbsp;|&nbsp; "
                        f"Category: {pt.task.category}{freq_badge}"
                    )
                else:
                    st.markdown(
                        f"🔲 **{pt.task.time}** &nbsp;|&nbsp; **{pt.task.name}** for {pt.pet.name} &nbsp;|&nbsp; "
                        f"{pt.task.duration_minutes} min &nbsp;|&nbsp; "
                        f"Priority: {priority_label} &nbsp;|&nbsp; "
                        f"Category: {pt.task.category}{freq_badge}"
                    )
            with col_btn:
                if not pt.task.is_completed:
                    if st.button("Done", key=f"complete_{task_key}_{i}"):
                        next_task = plan.scheduler.mark_task_complete(pt)
                        if next_task:
                            st.session_state.next_tasks[task_key] = next_task
                        st.rerun()

            # Show next-occurrence info for recurring tasks that were just completed
            if task_key in st.session_state.next_tasks:
                nt = st.session_state.next_tasks[task_key]
                st.caption(f"   ↳ Next **{nt.name}** scheduled for {nt.due_date} ({nt.frequency})")

        st.metric("Total scheduled time", f"{plan.total_duration} min")
    else:
        st.warning("No tasks could be scheduled — all tasks have conflicting time windows.")

    st.divider()
    st.subheader("Why this plan?")
    st.info(plan.explain_reasoning())

    if plan.skipped:
        st.subheader("Skipped tasks")
        st.caption("These tasks didn't fit within the available time for this day.")
        for pt in plan.skipped:
            priority_label = {1: "high", 2: "medium", 3: "low"}.get(pt.priority, str(pt.priority))
            st.markdown(
                f"⛔ **{pt.task.name}** for {pt.pet.name} &nbsp;|&nbsp; "
                f"{pt.task.duration_minutes} min &nbsp;|&nbsp; "
                f"Priority: {priority_label} &nbsp;|&nbsp; "
                f"Category: {pt.task.category}"
            )
