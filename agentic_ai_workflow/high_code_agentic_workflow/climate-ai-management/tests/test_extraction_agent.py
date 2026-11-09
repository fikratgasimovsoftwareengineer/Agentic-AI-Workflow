from climate_ai_management.agents.extraction_agent import build_extraction_agent


import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from uuid import uuid4
import json

from pathlib import Path
from dotenv import load_dotenv
project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / '.env')

APP_NAME = "climate_ai_management"
async def main():
    
    agent = build_extraction_agent(
        model="gemini-3.8-flash"
    )
    session_service = InMemorySessionService()
    
    runner = Runner(
        agent = agent,
        app_name= APP_NAME,
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
        Declared total emissions: 250 tCO2e
        Scope 3: Not reported
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
        
        if event.is_final_response():
            print("Final response: ", event.content)
            
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )
    
    extracted = session.state.get("extracted_data")
    
    print("\nDATI ESTRATTI:")
    print(json.dumps(extracted, indent=2, ensure_ascii=False))
    
if __name__ == "__main__":
    
    asyncio.run(main())