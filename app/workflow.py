from .models import EmployeeContext, OnboardingPlan
from .rules_engine import generate_base_plan
from .llm_engine import enrich_plan_with_llm
from .config import settings


def generate_onboarding_plan_workflow(ctx: EmployeeContext) -> OnboardingPlan:
    """
    Internal workflow orchestrator for OnboardGenie:
    1. Generate a rule-based base plan.
    2. Optionally enrich with IBM Granite (LLM).
    3. Return a complete, production-ready onboarding plan.
    """
    base_plan = generate_base_plan(ctx)

    if settings.USE_LLM:
        final_plan = enrich_plan_with_llm(ctx, base_plan)
    else:
        final_plan = base_plan

    return final_plan
