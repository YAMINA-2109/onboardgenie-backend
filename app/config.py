import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Central configuration object for the OnboardGenie backend.
    Reads environment variables once at startup.
    """

    # IBM / watsonx.ai configuration
    IBM_API_KEY: str | None = os.getenv("IBM_API_KEY")
    IBM_PROJECT_ID: str | None = os.getenv("IBM_PROJECT_ID")
    IBM_REGION: str | None = os.getenv("IBM_REGION", "eu-de")
    IBM_MODEL_ID: str | None = os.getenv(
        "IBM_MODEL_ID",
        "ibm/granite-3-8b-instruct",
    )

    # Feature flags
    USE_LLM: bool = os.getenv("USE_LLM", "false").lower() == "true"


settings = Settings()
