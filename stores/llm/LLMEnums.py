from enum import Enum

class LLMEnums(Enum):
    """Enum for LLM types."""
    OPENAI = "openai"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    LOCAL = "local"
    

class OpenAIEnums(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTENT = "assistent"