from .models import EmployeeContext, OnboardingPlan, OnboardingTask


def generate_base_plan(ctx: EmployeeContext) -> OnboardingPlan:
    """
    Pure rule-based onboarding engine.
    This guarantees structure, consistency and clear ownership,
    regardless of LLM availability.
    """
    phases = ["preboarding", "day1", "week1", "month1", "month2", "month3"]

    summary = (
        f"30-60-90 day onboarding plan for {ctx.employee_name} "
        f"as {ctx.role} in {ctx.department} at {ctx.location}, "
        f"starting on {ctx.start_date}. Focus on fast integration, "
        f"clarity on expectations, and progressive autonomy."
    )

    tasks: list[OnboardingTask] = []

    # PREBOARDING → HR + IT
    tasks.append(OnboardingTask(
        id="pre-1",
        phase="preboarding",
        title="Collect legal & HR documents",
        description="HR sends contract, confidentiality agreement and collects required documents.",
        owner="HR",
        due_offset_days=-5,
        channel="email",
    ))
    tasks.append(OnboardingTask(
        id="pre-2",
        phase="preboarding",
        title="Prepare IT access & tools",
        description="IT prepares laptop, email, VPN, project tools and required permissions.",
        owner="IT",
        due_offset_days=-3,
        channel="task",
    ))
    tasks.append(OnboardingTask(
        id="pre-3",
        phase="preboarding",
        title="Send welcome email with practical information",
        description=(
            f"Manager sends a friendly welcome email to {ctx.employee_name} with "
            "first-day logistics, schedule and expectations."
        ),
        owner="Manager",
        due_offset_days=-2,
        channel="email",
    ))

    # DAY 1 → HR + Manager
    tasks.append(OnboardingTask(
        id="d1-1",
        phase="day1",
        title="Company & culture introduction",
        description="HR presents company mission, culture, values and key policies.",
        owner="HR",
        due_offset_days=0,
        channel="meeting",
    ))
    tasks.append(OnboardingTask(
        id="d1-2",
        phase="day1",
        title="Team introduction & context",
        description=(
            "Manager introduces the team, explains ongoing projects and how "
            f"{ctx.role} will contribute."
        ),
        owner="Manager",
        due_offset_days=0,
        channel="meeting",
    ))

    # WEEK 1 → Manager + Employee
    tasks.append(OnboardingTask(
        id="w1-1",
        phase="week1",
        title="Define 30-60-90 day objectives",
        description="Manager and employee align on expectations, deliverables and success metrics.",
        owner="Manager",
        due_offset_days=3,
        channel="meeting",
    ))
    tasks.append(OnboardingTask(
        id="w1-2",
        phase="week1",
        title="Shadowing & first small tasks",
        description="Employee shadows teammates and takes ownership of low-risk tasks.",
        owner="Employee",
        due_offset_days=5,
        channel="task",
    ))

    # MONTH 1 → Employee
    tasks.append(OnboardingTask(
        id="m1-1",
        phase="month1",
        title="Deliver first impactful contribution",
        description="Employee delivers a first visible contribution aligned with team goals.",
        owner="Employee",
        due_offset_days=25,
        channel="task",
    ))

    # MONTH 3 → Manager + Employee
    tasks.append(OnboardingTask(
        id="m3-1",
        phase="month3",
        title="3-month review & growth plan",
        description="Manager and employee review progress and define next 6–12 months growth plan.",
        owner="Manager",
        due_offset_days=85,
        channel="meeting",
    ))

    suggested_meetings = [
        "Day-1 welcome meeting with HR",
        "Day-1 team introduction with manager",
        "Week-1 1:1 to define 30-60-90 day goals",
        "Month-3 review & growth conversation",
    ]

    learning_resources = [
        "Company handbook & HR policies",
        "Security & compliance training",
        f"Technical onboarding for {ctx.role} ({ctx.department})",
        "Internal knowledge base / documentation",
    ]

    return OnboardingPlan(
        employee=ctx,
        summary=summary,
        phases=phases,
        tasks=tasks,
        suggested_meetings=suggested_meetings,
        learning_resources=learning_resources,
    )
