import textwrap
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai import Credentials

from .models import EmployeeContext, OnboardingPlan
from .config import settings


def _get_granite_model() -> Model:
    """
    Initialize the IBM Granite model via watsonx.ai SDK.
    This is the single entry point to the LLM used by OnboardGenie.
    """
    api_key = settings.IBM_API_KEY
    project_id = settings.IBM_PROJECT_ID
    region = settings.IBM_REGION or "eu-de"
    model_id = settings.IBM_MODEL_ID or "ibm/granite-3-8b-instruct"

    if not api_key or not project_id:
        raise RuntimeError("IBM_API_KEY or IBM_PROJECT_ID is missing in environment variables")

    url = f"https://{region}.ml.cloud.ibm.com"

    creds = Credentials(url=url, api_key=api_key)
    model = Model(
        model_id=model_id,
        credentials=creds,
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 512,
            "temperature": 0.3,
        },
        project_id=project_id,
    )
    return model


def _build_email_prompt(plan: OnboardingPlan) -> str:
    """
    Prompt to generate a manager welcome email for the new hire.
    """
    e = plan.employee
    return textwrap.dedent(f"""
    You are OnboardGenie, an enterprise-grade HR onboarding assistant.

    Task:
    Write a warm, concise welcome email from the hiring manager
    to the new employee below.

    Employee:
    - Name: {e.employee_name}
    - Role: {e.role}
    - Department: {e.department}
    - Location: {e.location}
    - Start date: {e.start_date}

    Requirements:
    - Tone: friendly, professional, clear
    - Language: English
    - Style: HR-grade, corporate
    - Include a short welcome, first-day expectations, and who to contact for questions
    - Do not add explanations or comments around the email

    Return:
    Only the email body, including a subject line.
    """).strip()


def _build_manager_prompt(plan: OnboardingPlan) -> str:
    """
    Prompt to generate a 30-60-90 day manager briefing.
    """
    e = plan.employee
    return textwrap.dedent(f"""
    You are OnboardGenie, an HR coach for managers.

    Context:
    A new hire has just joined.

    Employee:
    - Role: {e.role}
    - Department: {e.department}
    - Seniority: {e.seniority_level}
    - Work mode: {e.work_mode}

    Current onboarding summary:
    {plan.summary}

    Task:
    Summarize what the manager should focus on during the first 90 days.

    Structure:
    - 30 days: focus on integration, trust, and clarity
    - 60 days: focus on ownership, feedback, and performance
    - 90 days: focus on autonomy, impact, and growth

    Output requirements:
    - Use clear bullet points starting with "- "
    - Keep it practical and actionable
    - Language: English, concise, executive-friendly
    - No extra explanation outside the bullet list
    """).strip()


def _build_learning_prompt(plan: OnboardingPlan) -> str:
    """
    Prompt to generate a learning path for the new hire.
    """
    e = plan.employee
    return textwrap.dedent(f"""
    You are OnboardGenie, a learning & development specialist.

    Employee profile:
    - Role: {e.role}
    - Department: {e.department}
    - Seniority: {e.seniority_level}

    Task:
    Design a short learning path for this new hire over the first 3 months.

    Structure it exactly as:
    - Week 1:
    - Weeks 2-4:
    - Months 2-3:

    Requirements:
    - Focus on what they must understand to be productive in this role
    - Mix company knowledge, tools, processes and technical skills
    - Language: English, concise and practical
    - Return ONLY the list above, no commentary
    """).strip()


def enrich_plan_with_llm(ctx: EmployeeContext, base_plan: OnboardingPlan) -> OnboardingPlan:
    """
    Enrich the rule-based onboarding plan with IBM Granite:
    - welcome email to the new hire
    - manager 30-60-90 briefing
    - learning path for the first 3 months
    """
    print("[LLM] enrich_plan_with_llm called, USE_LLM =", settings.USE_LLM)

    if not settings.USE_LLM:
        print("[LLM] LLM disabled, returning base plan only")
        return base_plan

    try:
        model = _get_granite_model()
    except Exception as e:
        print(f"[LLM] Granite initialization error: {e}")
        return base_plan

    # 1) Welcome email
    email_prompt = _build_email_prompt(base_plan)
    print("[LLM] Generating welcome email...")
    welcome_email = model.generate_text(prompt=email_prompt)

    # 2) Manager briefing
    manager_prompt = _build_manager_prompt(base_plan)
    print("[LLM] Generating manager briefing...")
    manager_briefing = model.generate_text(prompt=manager_prompt)

    # 3) Learning path
    learning_prompt = _build_learning_prompt(base_plan)
    print("[LLM] Generating learning path...")
    learning_path = model.generate_text(prompt=learning_prompt)

    enriched = base_plan.copy()
    enriched.welcome_email = welcome_email
    enriched.manager_briefing = manager_briefing
    enriched.learning_path = learning_path

    return enriched
