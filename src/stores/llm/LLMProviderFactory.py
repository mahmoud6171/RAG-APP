from .LLMEnums import LLMEnums
from .providers import OpenAIProvider, CoHereProvider

class LLMProviderFactory:
    """Factory class for creating LLM providers."""
    
    def __init__(self,config :dict):
        self.config = config
        
    
    
    def create_provider(self,provider_type: str):
        """Creates an LLM provider based on the provider type."""
        if provider_type == LLMEnums.OPENAI.value:  
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                #api_url=self.config.api_url,
                default_max_input_tokens=self.config.INPUT_MODEL_MAX_CHARACTERS,
                default_max_output_tokens=self.config.GENERATION_MODEL_MAX_TOKENS,
                tempreture=self.config.GENERATION_MODEL_TEMPERATURE
            )
        elif provider_type == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_max_input_tokens=self.config.INPUT_MODEL_MAX_CHARACTERS,
                default_max_output_tokens=self.config.GENERATION_MODEL_MAX_TOKENS,
                tempreture=self.config.GENERATION_MODEL_TEMPERATURE
            )
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")