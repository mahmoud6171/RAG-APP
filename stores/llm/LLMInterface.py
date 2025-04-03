from abc import ABC, abstractmethod

class LLMInterface(ABC):
    """
    Abstract base class for all LLM (Large Language Model)
    implementations. This class defines the interface that all LLMs must implement.
    """
    @abstractmethod
    def set_generation_model(self, model_id: str):
        pass
    
    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size:int):
        pass
    
    @abstractmethod
    def generate_response(self, prompt: str, chat_history:list ,max_output_tokens:int,
                                temprture :float ):
        """
        Generate a response based on the provided prompt.
        """
        pass
    
    @abstractmethod
    def generate_embedding(self, text: str, document_type:str,):
        """
        Generate an embedding for the provided text.
        """
        pass
    
    @abstractmethod
    def constract_prompt(self, prompt: str, role: str) -> str:
        """
        Construct a prompt by combining the provided prompt and context.
        """
        pass