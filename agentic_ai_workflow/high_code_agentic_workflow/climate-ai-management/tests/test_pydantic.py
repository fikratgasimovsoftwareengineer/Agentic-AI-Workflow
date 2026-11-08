from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(extra='forbid')  

    name: str="Fikret"

user = User()  
print(user)
#> name='John Doe'