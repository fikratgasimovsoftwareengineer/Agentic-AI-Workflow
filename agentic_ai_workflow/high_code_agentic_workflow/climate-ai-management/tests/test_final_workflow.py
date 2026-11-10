from climate_ai_management.agents.workflow import build_workflow


import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from uuid import uuid4
import json
from climate_ai_management.agent import app

from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / '.env')

APP_NAME = app.name


async def main():
    
    """ agent = build_workflow(
        model="gemini-3.8-flash"
    ) """
    session_service = InMemorySessionService()
    
    runner = Runner(
        app= app,
        session_service=session_service
    )
    
    session_id = str(uuid4())
    user_id = "test_user"
    
    await session_service.create_session(
        app_name = APP_NAME,
        user_id=user_id,
        session_id=session_id
    )
        
    
    document = """
    Company: Demo Company
    Reporting year: 2025
    Scope 1: 120 tCO2e
    Scope 2: 80 tCO2e
    Scope 3: 15 tCO2e
    Declared total emissions: 250 tCO2e
    """
    message = types.Content(
        role = "user",
        parts=[types.Part(text=document)]
    )
    
    async for event in runner.run_async(
        session_id=session_id,
        user_id=user_id,
        new_message=message
    ):
        
        if event.actions and event.actions.state_delta:
            print("State changes: ")
            print(
                json.dumps(
                    event.actions.state_delta,
                    indent=2,
                    ensure_ascii=False,
                    default=str
                )
            )
        
        if event.is_final_response() and event.content:
            print("Final response: ", event.content)
            
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )
    
    state = dict(session.state)

    output_path = PROJECT_ROOT / "public/data/dati.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(
            state,
            indent=4,
            ensure_ascii=False,
            default=str,
        ),
        encoding="utf-8",
    )

    print("\nSESSION STATE:")
    print(json.dumps(state, indent=2, ensure_ascii=False, default=str))

    print("\nSaved to:", output_path)
        
        
if __name__ == "__main__":
    
    asyncio.run(main())