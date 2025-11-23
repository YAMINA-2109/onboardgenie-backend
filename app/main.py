from fastapi import FastAPI

from .models import EmployeeContext, OnboardingPlan, OnboardingRequest
from .workflow import generate_onboarding_plan_workflow

app = FastAPI(
    title="OnboardGenie API",
    description="Generates enterprise-grade 30-60-90 day onboarding plans for new employees.",
    version="2.0.0",
)


@app.get("/health")
def health_check():
    """
    Simple health-check endpoint for monitoring and deployment checks.
    """
    return {"status": "ok", "service": "OnboardGenie API v2"}


@app.post("/onboarding/plan", response_model=OnboardingPlan)
def generate_onboarding_plan(req: OnboardingRequest):
    """
    Main endpoint used by IBM watsonx Orchestrate as a custom skill.

    1. Accepts an OnboardingRequest (camelCase, OpenAPI / Orchestrate-friendly).
    2. Maps it to an internal EmployeeContext.
    3. Executes the internal workflow (rules + optional LLM enrichment).
    4. Returns a structured onboarding plan for the new hire.
    """
    ctx = EmployeeContext(
        employee_name=req.employeeName,
        role=req.role,
        department=req.department,
        location=req.location or "Unknown",
        start_date=req.startDate,
        seniority_level=req.level or "junior",
        work_mode=req.workMode or "hybrid",
    )

    plan = generate_onboarding_plan_workflow(ctx)
    return plan