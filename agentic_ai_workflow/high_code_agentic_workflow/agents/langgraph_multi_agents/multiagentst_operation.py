from langchain_ollama import OllamaLLM
from langchain_core import ToolMessage ## Message for passing the result of executing a tool back to a model.
from langchain_core.tools import tools

model = OllamaLLM(model="llama3.2",
                  temperature=0.3,
                  num_predict=2048,
                  top_p=0.9)

input_text = "The meaning of life is "
response = model.invoke(input_text)
print(response)

for chunk in model.astream (input_text):
    print(chunk, end="")
