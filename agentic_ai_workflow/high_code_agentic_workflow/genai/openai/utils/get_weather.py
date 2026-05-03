import json

def get_current_weather(location:str):
    
    if "milano" in location.lower():
        return json.dumps({"location":"Milano", "temperature":25})
    
    elif "parigi" in location.lower():
        return json.dumps({"location":"Parigi", "temperature":15})
    
    else:
        return json.dumps({"location":location, "temperature":"sconosciuto"})