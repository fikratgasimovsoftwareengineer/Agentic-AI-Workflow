from domain.runner import RunnerOrchestrator
import asyncio


def route_query(query:str)->str:
    
    q = query.lower()
    weather_keywords = ["weather", "forecast", "rain", "temperature", "hiking"]
    if any(k in q for k in weather_keywords):
        return "weather"
    return "day_trip"

async def main():
    
    orchestrator = RunnerOrchestrator()   
    
    while True:
        user_query = input('Enter question :? \n').strip()
        if user_query.lower() =='exit':
            break
        
        if not user_query:
            continue
        
        if route_query(query = user_query) == 'weather':
            await orchestrator.run_weather_agent(user_query)
            
        else:
            await orchestrator.run_day_trip_genie(user_query)
    
    
if __name__ == "__main__":
    asyncio.run(main())
    

    # Note the new budget constraint in the query!
    query = "Plan a relaxing and artsy day trip near Sunnyvale, CA. Keep it affordable!"
    print(f"🗣️ User Query: '{query}'")
    
    query = "I want to go hiking near Lake Tahoe, what's the weather like?"
    print(f"🗣️ User Query: '{query}'")