from .LLMEnums import LLMEnums
from ..providers import OpenAIProvider, CoHereProvider

class LLMProviderFactory:
    """Factory class for creating LLM providers."""
    
    def __init__(self,config :dict):
        self.config = config
        
    
    @staticmethod
    def create_provider(self,provider_type: str):
        """Creates an LLM provider based on the provider type."""
        if provider_type == LLMEnums.OPENAI.value:  
            return OpenAIProvider(
                api_key=self.config.api_key,
                api_url=self.config.api_url,
                default_max_input_tokens=self.config.default_max_input_tokens,
                default_max_output_tokens=self.config.default_max_output_tokens,
                tempreture=self.config.tempreture
            )
        elif provider_type == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.api_key,
                default_max_input_tokens=self.config.default_max_input_tokens,
                default_max_output_tokens=self.config.default_max_output_tokens,
                tempreture=self.config.tempreture
            )
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")