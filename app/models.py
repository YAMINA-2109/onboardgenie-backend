from pydantic import BaseModel
from typing import List, Optional


class EmployeeContext(BaseModel):
    """
    Internal normalized representation of the employee profile.
    This is what the rules engine and LLM use.
    """

    employee_name: str
    role: str
    department: str
    location: str
    start_date: str           # ISO date string or human-readable date
    seniority_level: str      # "junior", "mid", "senior"
    work_mode: str            # "remote", "hybrid", "onsite"


class OnboardingTask(BaseModel):
    """
    Single onboarding task assigned to HR, IT, Manager or Employee.
    """

    id: str
    phase: str                # "preboarding", "day1", "week1", ...
    title: str
    description: str
    owner: str                # "HR", "IT", "Manager", "Employee", ...
    due_offset_days: int      # relative to start_date
    channel: Optional[str] = None   # "email", "task", "meeting", ...


class OnboardingPlan(BaseModel):
    """
    Full onboarding plan returned by the API and consumed by Orchestrate:
    - rule-based structure
    - optionally enriched by IBM Granite LLM.
    """

    employee: EmployeeContext
    summary: str
    phases: List[str]
    tasks: List[OnboardingTask]
    suggested_meetings: List[str]
    learning_resources: List[str]

    # LLM-enriched fields
    welcome_email: Optional[str] = None
    manager_briefing: Optional[str] = None
    learning_path: Optional[str] = None


class OnboardingRequest(BaseModel):
    """
    Input model that matches the OpenAPI schema used by watsonx Orchestrate.
    This is the "external" contract (camelCase field names).
    """

    employeeName: str
    role: str
    department: str
    startDate: str

    level: Optional[str] = None
    location: Optional[str] = None
    workMode: Optional[str] = None
    managerName: Optional[str] = None
    language: Optional[str] = None
    contractType: Optional[str] = None
    toolsNeeded: Optional[List[str]] = None
    onboardingGoals: Optional[List[str]] = None
    roleContext: Optional[str] = None
    customNotes: Optional[str] = None
