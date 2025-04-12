from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging


class OpenAIProvider(LLMInterface):
    def __init__(self,api_key:str, api_url:str = None,
                 default_max_input_tokens:int =1000,
                 default_max_output_tokens:int =1000,
                 tempreture :float =0.3,):
        
        self.api_key = api_key
        self.api_url = api_url
        self.default_max_input_tokens = default_max_input_tokens
        self.default_max_output_tokens = default_max_output_tokens
        self.tempreture = tempreture
        
        self.generation_model_id = None
        
        self.embedding_model_id = None
        self.embedding_size = None
        
        self.client = OpenAI(
            api_key = self.api_key,
            #api_url = self.api_url
        )
        
        self.logger = logging.getLogger(__name__)
        
        
    def set_generation_model(self, model_id):
        self.generation_model_id = model_id
        
    def set_embedding_model(self, model_id :str, embedding_size:int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        
    def generate_response(self, prompt:str, chat_history:list=[] ,
                                max_output_tokens :int =None, temprture :int =None):
        
        if not self.client:
            self.logger.error("OpenAi client wasnt set")
            return None
        
        if not self.generation_model_id:
            self.logger.error("generataion model id for OpenAi client wasnt set")
            return None
        

        max_output_tokens = max_output_tokens if  max_output_tokens else self.default_max_output_tokens 
        temprture = temprture if temprture else self.tempreture
        
        chat_history.append(
            self.constract_prompt(prompt=prompt, role=OpenAIEnums.USER.value)
        )
        
        response = self.client.responses.create(
            model= self.generation_model_id,
            input = chat_history,
            max_output_tokens=max_output_tokens,
            temperature=temprture
        )
        if not response or not response.output_text :
            self.logger.error("Error while generating text with OpenAI")
            return None
        

        return response.output_text
        
    def process_input_text(self, text: str):
        return text[:self.default_max_input_tokens].strip()
    
    def generate_embedding(self, text, document_type):
        if not self.client:
            self.logger.error("OpenAi client wasnt set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("embedding model if for OpenAi client wasn't set")
            return None
        
        response = self.client.embeddings.create(
            model= self.embedding_model_id,
            input= text
        )
        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error while embedding text with OpenAI")
            return None

        
        return response.data[0].embedding
    
    def constract_prompt(self, prompt:str, role:str):
        return{
            "role":role,
            "content":self.process_input_text(prompt)
        }