# OnboardGenie – AI-Powered 30-60-90 Day Onboarding Assistant

OnboardGenie is an AI-powered HR assistant that generates expert-level, structured 30-60-90 day onboarding plans for new hires.  
It connects a Python backend (FastAPI) with an IBM watsonx Orchestrate agent to deliver a complete onboarding experience:
- Preboarding → Day 1 → Week 1 → Month 1 → Month 2 → Month 3
- Detailed tasks for HR, IT, manager, and the new employee
- Personalized welcome email
- Manager briefing (focus points for 30/60/90 days)
- Learning path for the first three months

This project was built for an AI hackathon to demonstrate how LLMs + orchestration tools can streamline and standardize employee onboarding at scale.

---

## 🚀 Key Features

- **AI-generated 30-60-90 day onboarding plan**
  - Phases: preboarding, day 1, week 1, month 1, month 2, month 3
  - Tasks with owner, due date offset, and channel (email, meeting, task, etc.)
- **Personalized welcome email**
  - Tailored to the employee’s name, role, department, and start date
- **Manager briefing**
  - Clear focus points for 30 / 60 / 90 days (integration, ownership, autonomy, growth)
- **Learning path**
  - Progressive learning steps over the first 3 months (tools, stack, AI/ML concepts, internal process)
- **Production-ready backend**
  - FastAPI service deployed on Render
  - OpenAPI 3.0 specification used as a tool in IBM watsonx Orchestrate
- **Enterprise-grade orchestration**
  - IBM watsonx Orchestrate agent (“OnboardGenie”) that:
    - Calls the backend tool when an onboarding plan is requested
    - Summarizes, reformats, and explains plans for HR, managers, and employees

---

## 🧱 Architecture

**High-level components:**

1. **FastAPI Backend (OnboardGenie API)**
   - Exposes one main endpoint: `POST /onboarding/plan`
   - Takes a rich employee context (name, role, start date, level, location, etc.)
   - Returns a structured `OnboardingPlanResponse` (employee, phases, tasks, meetings, resources, emails, learning path)
   - Deployed on Render:  
     `https://onboardgenie-api.onrender.com`

2. **OpenAPI Specification (`onboardgenie.yaml`)**
   - Describes the backend using OpenAPI 3.0.3
   - Defines:
     - `OnboardingRequest` schema (input)
     - `OnboardingPlanResponse` schema (output)
     - Endpoint `POST /onboarding/plan`
   - Imported into IBM watsonx Orchestrate as a **tool** called `GenerateOnboardingPlan`.

3. **IBM watsonx Orchestrate Agent (“OnboardGenie”)**
   - Uses the LLM model `llama-3-2-90b-vision-instruct` (or similar)
   - Has a system-level Behavior configuration:
     - Always call the `GenerateOnboardingPlan` tool when an onboarding plan is requested
     - Enrich results with clear explanations, summaries, and messages
   - Exposed through the Orchestrate chat UI.

---

## 🛠 Tech Stack

- **Backend**
  - Python 3
  - FastAPI
  - Uvicorn
  - Pydantic
- **Deployment**
  - Render (Free tier)
- **AI / Orchestration**
  - IBM watsonx Orchestrate
  - LLM model (Llama-3 / watsonx)
  - OpenAPI 3.0.3 tool integration

---

## 📡 API – OnboardGenie Backend

### Base URL

```text
https://onboardgenie-api.onrender.com
````

### Endpoint

#### `POST /onboarding/plan`

Generate a full 30-60-90 day onboarding plan for a new employee.

**Request body (`application/json`):**

```json
{
  "employeeName": "Mina Atm",
  "role": "AI developer",
  "department": "IA/ML",
  "startDate": "2025-12-12",
  "level": "junior",
  "location": "France",
  "workMode": "hybrid",
  "managerName": "Lisa",
  "language": "english",
  "contractType": "CDI",
  "toolsNeeded": [
    "Laptop",
    "VPN access",
    "GitHub",
    "Jira"
  ],
  "onboardingGoals": [
    "Be ready to start coding within the first month",
    "Understand the product architecture"
  ],
  "roleContext": "Junior AI developer working on LLM-based internal tools.",
  "customNotes": "Needs extra support on cloud tooling during month 1."
}
```

**Response (simplified):**

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
  "tasks": [
    {
      "id": "pre-1",
      "phase": "preboarding",
      "title": "Collect legal & HR documents",
      "description": "HR sends contract, confidentiality agreement and collects required documents.",
      "owner": "HR",
      "due_offset_days": -5,
      "channel": "email"
    }
    // ...
  ],
  "suggested_meetings": [
    "Day-1 welcome meeting with HR",
    "Week-1 1:1 to define 30-60-90 day goals"
  ],
  "learning_resources": [
    "Company handbook & HR policies",
    "Security & compliance training"
  ],
  "welcome_email": "Subject: Welcome to the IA/ML Team, Mina! ...",
  "manager_briefing": "Manager focus for Mina's first 90 days: ...",
  "learning_path": "Week 1: ... Months 2-3: ..."
}
```

---

## 🧪 Run the Backend Locally (Dev Mode)

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/onboardgenie-backend.git
cd onboardgenie-backend

# 2. Create and activate a virtual environment (optional but recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the FastAPI server
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
http://localhost:8000/docs   (Swagger UI)
```

---

## 🤖 IBM watsonx Orchestrate Integration

1. **Create a new agent** in Orchestrate named `OnboardGenie`.

2. In **Toolset**, add a new tool from an **OpenAPI document** and import `onboardgenie.yaml`.

3. Confirm that the tool `GenerateOnboardingPlan` is created and mapped to:

   * `POST /onboarding/plan`
   * Request body: `OnboardingRequest`
   * Response: `OnboardingPlanResponse`

4. In the **Behavior → Instructions** section, set the system rules, for example:

   ```text
   - If the user asks for an onboarding plan → ALWAYS call the tool GenerateOnboardingPlan.
   - If the user asks for summaries or explanations → provide them directly.
   - When interacting with HR or managers → be formal and actionable.
   - When interacting with employees → be supportive, clear, and friendly.
   ```

5. Click **Deploy** so the agent becomes available in the Orchestrate chat.

---

## 🎬 Demo Scenario for the Jury

1. Open the **Orchestrate Chat** with the `OnboardGenie` agent.

2. Type:

   > “Generate a complete onboarding plan for a new AI developer named Mina, joining the IA/ML team in France next month, working in hybrid mode, junior level.”

3. Show the agent:

   * Calling the `GenerateOnboardingPlan` tool.
   * Returning a structured onboarding plan + tasks + meetings.
   * Displaying a personalized welcome email, manager briefing, and learning path.

4. Optionally, ask follow-up questions:

   * “Summarize this onboarding as 5 key bullet points for the CEO.”
   * “Rewrite the welcome email in French.”
   * “Adapt the plan for a remote senior engineer.”

This demonstrates orchestration, tool usage, and LLM reasoning in a real HR use case.

---

## 🔮 Future Improvements

* Add company-specific knowledge bases (HR policies, security training, internal wiki) as Knowledge sources.
* Generate calendar events and tasks directly in Outlook or Slack.
* Add a voice channel (phone / audio) using the Voice modality.
* Support multiple languages out of the box (English, French, etc.).
* Analytics dashboard to track onboarding progress and task completion.

---

## 👩‍💻 Author

* **Name:** Yamina Atmaoui
* **Role:** AI & Full-Stack Developer
* **Hackathon:** IBM / watsonx – AI Automation & Orchestration

```
