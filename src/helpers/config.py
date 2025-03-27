from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List
class Settings(BaseSettings):

    APP_NAME: str = Field(..., description="The name of the application",)
    APP_VERSION: str = Field(..., description="The version of the application")
    OPENAI_KEY: str = Field(..., description="OpenAI API Key")
    FILE_ALLOWED_TYPES: List[str] = Field(..., description="List of allowed file types")
    FILE_MAX_SIZE: int = Field(..., description="File size in bytes", )  
    FILE_DEFAULT_CHUNK_SIZE: int = Field(..., description="Default chunk size for file upload", )
    
    MONGODB_URL :str
    MONGODB_DATABASE :str
   
    
    model_config = SettingsConfigDict(env_file=".env")
    

def get_settings(): 
    return Settings()