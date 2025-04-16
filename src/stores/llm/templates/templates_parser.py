import os

class Template_Parser:
    
    def __init__(self,language: str =None,default_language: str = "en"):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = None
        
        self.set_language(language)
    
    
    def set_language(self, language):
        if not language:
            self.language = self.default_language
         
        language_path= os.path.join(self.current_path,"locales",language)
        if os.path.exists(language_path):
            self.language = language
            
        else:
            self.language = self.default_language
            
    def get(self, group:str, key:str, vars:dict={}):
        if not group or not key:
            return None
        group_path = os.path.join(self.current_path,"locales",self.language,f"{group}.py")
        target_language = self.language
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path,"locales",self.default_language,f"{group}.py")
            target_language = self.default_language
            
        if not os.path.exists(group_path):
            return None
        
        #import group module 
        module = __import__(f"stores.llm.templates.locales.{target_language}.{group}",fromlist=[group])
        
        if not module:
            return None
        
        key_attrabiute = getattr(module,key)
        return key_attrabiute.substitute(vars)
        
            
        