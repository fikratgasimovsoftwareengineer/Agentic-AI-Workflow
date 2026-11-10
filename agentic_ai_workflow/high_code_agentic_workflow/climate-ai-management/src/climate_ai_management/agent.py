import os
from pathlib import Path

from dotenv import load_dotenv

from google.adk.apps import App
from google.adk.integrations.model_armor import (
    ModelArmorConfig,
    ModelArmorPlugin,
)

from climate_ai_management.agents.workflow import build_workflow


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = os.environ["GOOGLE_CLOUD_MODEL_ARM_REGION"]

PROMPT_TEMPLATE = (
    f"projects/{PROJECT_ID}/locations/{REGION}/"
    "templates/climate-prompt-guardrails"
)

RESPONSE_TEMPLATE = (
    f"projects/{PROJECT_ID}/locations/{REGION}/"
    "templates/climate-response-guardrails"
)

root_agent = build_workflow(
    model="gemini-3.8-flash"
)

model_armor_plugin = ModelArmorPlugin(
    config=ModelArmorConfig(
        prompt_template_name=PROMPT_TEMPLATE,
        response_template_name=RESPONSE_TEMPLATE,

        input_blocked_message=(
            "Please try to clear out your request , otherswise your request is blocked by Climate AI Management security policy."
        ),

        output_blocked_message=(
            "Model answer is not aligned with user request, therefore it is  blocked by Climate AI Management security policy."
        ),

        block_on_screening_failure=True,
    )
)

app = App(
    name="climate_ai_management",
    root_agent=root_agent,
    plugins=[model_armor_plugin],
)