from pathlib import Path
from dotenv import load_dotenv

# Load project configuration
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

from climate_ai_management.agents.workflow import build_workflow

# Entry point discovered by ADK Web
root_agent = build_workflow(
    model="gemini-3.8-flash"
)