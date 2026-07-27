from google.genai.types import Content, Part
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session

### custom agents ###
from agents.day_trip_agent import DayTripAgent
from agents.weather_agent import WeatherAgent
### tools ##3
from tools.duck_web_search import DuckWebSearch



class RunnerOrchestrator:
    
    def __init__(self):
        self.session_service = InMemorySessionService()
        self.web_search = DuckWebSearch()
        self.day_trip_agent = DayTripAgent(self.web_search)
        self.weather_agent = WeatherAgent()
      
        self.my_user_id = "fikret_id_001"
        
        
    # --- A Helper Function to Run Our Agents ---
    # We'll use this function throughout the notebook to make running queries easy.
    async def run_agent_query(self, agent:Agent, query:str, session:Session, user_id:str, is_router:bool=False):
        print(f"\n🚀 Running query for agent: '{agent.name}' in session: '{session.id}'...")

        runner = Runner(
            agent = agent,
            session_service = self.session_service,
            app_name = agent.name,
        )

        final_response = ""
        though_response = ""
        try:
            async for event in runner.run_async(
                user_id = user_id,
                session_id = session.id,
                new_message = Content(parts = [Part(text=query)], role="user")
            ):
                if not is_router:
                    print(f"event: {event}")
                if event.is_final_response() and event.content and event.content.parts:
                    for p in event.content.parts:
                        if p.text and getattr(p, 'thought', False):
                            final_response = p.text
                        else:
                            though_response = p.text
                            
                        
                #return final_response, though_response
            
        except Exception as e:
            final_response = f"An error occured :{e}"
            

        if not is_router:
            print("\n" + "-"*50)
            print("✅ Final Response:")
            print(final_response)
            print("-"*50 + "\n")
            
            print("==============REASONIG=======================")
            print(f"{though_response}\n")
            print("                                              ")

        return final_response, though_response
    
    # --- Let's test the Day Trip Genie! ---
    async def run_day_trip_genie(self, query:str):
        # Create a new, single-use session for this query
        day_trip_session = await self.session_service.create_session(
            app_name=self.day_trip_agent.name,
            user_id=self.my_user_id
        )

        return await self.run_agent_query(self.day_trip_agent, 
                                          query,
                                          day_trip_session, 
                                          self.my_user_id)


                
    ################################################################33
    ####  WEATHER AGENT ###
    async def run_weather_agent(self, query:str):
        weather_session = await self.session_service.create_session(app_name=self.weather_agent.name,
                                                                    user_id=self.my_user_id)
        
        return await self.run_agent_query(self.weather_agent, 
                                          query,
                                          weather_session, 
                                          self.my_user_id)
