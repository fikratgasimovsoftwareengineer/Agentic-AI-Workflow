import requests

url = "https://v2.jokeapi.dev/joke/Any?safe-mode&type=twopart"



## ai llm endpoint
API_URL = "http://nexusraven.nexusflow.ai"

headers = {
        "Content-Type": "application/json"
}

USER_QUERY = "Hey! Can you get me a joke for this december?"

def extract_joke():
    

    response = requests.get(url)

    print(response.json()["setup"])
    print(response.json()["delivery"])
    
    return response

def get_joke(category: str = "Any"):
    """
    Fetches a funny joke from the JokeAPI.
    Supports categories such as Any, Programming, Pun, Christmas.
    """
    url = f"https://v2.jokeapi.dev/joke/{category}?safe-mode&type=twopart"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        if data.get("error"):
            return f"Error  from Joke API {data.get('message')}"
        return f"{data['setup']}\n{data['delivery']}"
    
    except Exception as e:
        return f"Errore nel recupero della barzelletta: {e}"
    except KeyError:
        return  "Error: Invalid joke format from API"        
    
def raven_post(payload):
	"""
	Sends a payload to a TGI endpoint.
    ### Parameters
    - payload: The payload to send to the TGI endpoint.
    ### Returns
    - The response from the TGI endpoint.
	"""
	import requests
    ### RAVEN POST ENDPOINT
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


def query_raven(prompt):
	"""
	This function sends a request to the TGI endpoint to get Raven's function call.
	This will not generate Raven's justification and reasoning for the call, to save on latency.
	"""
	
	output = raven_post({
		"inputs": prompt,
		"parameters" : {"temperature" : 0.001, "stop" : ["<bot_end>"], "do_sample" : False, "max_new_tokens" : 2048, "return_full_text" : False}})
	call = output[0]["generated_text"].replace("Call:", "").strip()
	return call

