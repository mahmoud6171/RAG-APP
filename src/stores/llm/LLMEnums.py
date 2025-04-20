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
    
    
class CoHereEnums(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTENT = "assistent"
    
    QUERY = "search_query"
    DOCUMENT = "search_document"
    IMAGE = "image"
    
    
class DocumentTypeEnums(Enum):
    """Enum for document types."""
    IMAGE = "image"
    DOCUMENT = "document"
    QUERY = "query"