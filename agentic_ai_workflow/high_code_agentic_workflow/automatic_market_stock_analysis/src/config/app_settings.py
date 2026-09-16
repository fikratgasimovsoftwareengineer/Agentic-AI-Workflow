from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", 
                                     env_file_config="utf-8",
                                     extra="ignore")
    
    ollama_base_url:str = "http://localhost:11434"
    ollama_model:str = "qwen3:8b"
    
    langsmith_tracing:bool = False
    langsmith_api_key:str = ""
    langsmith_project:str = "agentic-foundations"
    