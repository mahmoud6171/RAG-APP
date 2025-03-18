from pydantic_settings import BaseSettings,SettingsConfigDict
class Setting(BaseSettings):
    
    APP_Name : str
    APP_Version : str 
    OPENAI_KEY : str
    
    
    class config:
        env_file = ".env"
        
def get_setting():
    return Setting()