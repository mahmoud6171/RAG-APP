from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereEnums
import cohere 
import logging

class CoHereProvider(LLMInterface):
    def __init__(self, api_key:str, api_url:str = None,
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
        
        self.client = cohere.ClientV2(self.api_key)
        
        self.logger = logging.getLogger(__name__)
    
    
    def set_generation_model(self, model_id):
        self.generation_model_id = model_id
        
    def set_embedding_model(self, model_id :str, embedding_size:int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        
    def process_input_text(self, text: str):
        return text[:self.default_max_input_tokens].strip()
    
    def generate_response(self, prompt: str, chat_history:list ,max_output_tokens:int, temprture :float ):
        if not self.client:
            self.logger.error("OpenAi client wasnt set")
            return None
        
        if not self.generation_model_id:
            self.logger.error("generataion model id for OpenAi client wasnt set")
            return None
        

        max_output_tokens = max_output_tokens if  max_output_tokens else self.default_max_output_tokens 
        temprture = temprture if temprture else self.tempreture
        
        chat_history.append(
            self.constract_prompt(prompt=prompt, role=CoHereEnums.USER.value)
        )
        response = self.client.chat(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temprture
        )
        if not response or not response.message or len(response.message.content)==0 or not response.message.content[0].text :
                self.logger.error("Error while generating text with OpenAI")
                return None

        return response.message.content[0].text
    
    
        
    def generate_embedding(self, text : str, document_type :str):
        if not self.client:
            self.logger.error("CoHere client wasnt set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("embedding model  for CoHere client wasnt set")
            return None
        
        input_type = CoHereEnums.DOCUMENT.value 
        if document_type == CoHereEnums.QUERY.value:
            input_type = CoHereEnums.QUERY.value
            
        
        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_input_text(text)],
            input_type=input_type,
            embedding_types=["float"],
        )
        
        
        if not response or not response.embeddings or  not response.embeddings.float:
            self.logger.error("Error while embedding text with Cohere")
            return None
        
        return response.embeddings.float[0]
        
    
    def constract_prompt(self, prompt:str, role:str):
        return{
            "role":role,
            "content":self.process_input_text(prompt)
        }