# OnboardGenie – AI-Powered Onboarding Engine (IBM watsonx)

OnboardGenie is an enterprise-grade onboarding engine designed for HR and PeopleOps teams.  
It generates structured **30-60-90 day onboarding plans** for new hires and enriches them using **IBM watsonx.ai (Granite)**.

This backend is exposed as a REST API and can be plugged into **IBM watsonx Orchestrate** as a **custom OpenAPI tool**.

---

## ✨ What OnboardGenie Does

- **Rule-based onboarding engine**

  - Phases: `preboarding`, `day1`, `week1`, `month1`, `month2`, `month3`
  - Clear ownership: **HR, IT, Manager, Employee**
  - Structured output: tasks, meetings, learning resources

- **LLM enrichment with IBM Granite**

  - Personalized **welcome email** for the new hire
  - Manager **30-60-90 briefing**
  - **Learning path** for the first 3 months

- **Orchestrate-ready**
  - Single endpoint: `POST /onboarding/plan`
  - Request model aligned with your OpenAPI schema (camelCase → Pydantic)
  - Can be registered as a tool: `GenerateOnboardingPlan` in IBM watsonx Orchestrate

---

## 🧱 Architecture

```text
backend/
  app/
    __init__.py
    config.py        # env & IBM settings
    models.py        # Pydantic models (request / response / internal types)
    rules_engine.py  # rule-based onboarding plan generation
    llm_engine.py    # IBM Granite integration (welcome email, briefing, learning path)
    workflow.py      # internal orchestrator (rules + LLM)
    main.py          # FastAPI app (health + /onboarding/plan)
   openapi/
     onboardgenie.yaml
  .gitignores
  requirements.txt
  README.md
```

- **FastAPI** exposes the HTTP API.
- **rules_engine** guarantees a consistent base plan.
- **llm_engine** calls **IBM Granite** via the `ibm-watsonx-ai` SDK.
- **workflow** decides whether to enrich with LLM based on `USE_LLM`.

---

## ⚙️ Configuration

Environment variables are loaded via `.env` (with `python-dotenv`).

Create a `.env` file in `backend/`:

```env
USE_LLM=true

IBM_API_KEY=your_ibm_api_key
IBM_PROJECT_ID=your_project_id
IBM_REGION=eu-de              # or us-south, etc.
IBM_MODEL_ID=ibm/granite-3-8b-instruct
```

---

## 📦 Local Installation

From the `backend/` folder:

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the API
uvicorn app.main:app --reload --port 8080
```

The API will be available at:

- Swagger UI: [http://localhost:8080/docs](http://localhost:8080/docs)
- Health check: [http://localhost:8080/health](http://localhost:8080/health)

---

## 🧪 Example Request

`POST /onboarding/plan`

```json
{
  "employeeName": "Mina Atm",
  "role": "AI developer",
  "department": "IA/ML",
  "startDate": "2025-12-12",
  "level": "junior",
  "location": "France",
  "workMode": "hybrid"
}
```

Example response (simplified):

```json
{
  "employee": {
    "employee_name": "Mina Atm",
    "role": "AI developer",
    "department": "IA/ML",
    "location": "France",
    "start_date": "2025-12-12",
    "seniority_level": "junior",
    "work_mode": "hybrid"
  },
  "summary": "30-60-90 day onboarding plan for Mina...",
  "phases": ["preboarding", "day1", "week1", "month1", "month2", "month3"],
  "tasks": [ ... ],
  "suggested_meetings": [ ... ],
  "learning_resources": [ ... ],
  "welcome_email": "Subject: Welcome to the IA/ML Team, Mina!...",
  "manager_briefing": "- 30 days: ...",
  "learning_path": "- Week 1: ..."
}
```

---

## 🧩 Integration with IBM watsonx Orchestrate

OnboardGenie is designed to be used as a **custom OpenAPI tool**:

1. **Deploy** this backend to a public URL, e.g.:

   ```text
   https://onboardgenie-api.onrender.com
   ```

2. In your OpenAPI YAML for Orchestrate, set:

   ```yaml
   openapi: 3.0.3
   servers:
     - url: https://onboardgenie-api.onrender.com
       description: OnboardGenie production API
   paths:
     /onboarding/plan:
       post:
         operationId: GenerateOnboardingPlan
         ...
   ```

3. **Import** the OpenAPI spec into **IBM watsonx Orchestrate** as a tool:

   - Tool name: `GenerateOnboardingPlan`
   - Method: `POST /onboarding/plan`

4. Use that tool inside your Orchestrate agent alongside:

   - Email skills (send welcome email)
   - Task/Project skills
   - Calendar skills (for meetings)

---

## 📜 API Contract (OpenAPI)

The full OpenAPI contract used by IBM watsonx Orchestrate
is available in the repository:

/openapi/onboardgenie.yaml

This file declares:

- request/response model
- the `POST /onboarding/plan` operation
- schema definitions
- server URL (updated after deployment)

This YAML file is the contract imported inside Orchestrate
as the custom tool **GenerateOnboardingPlan**.
