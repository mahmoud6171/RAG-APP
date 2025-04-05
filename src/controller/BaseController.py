import random
import string
from helpers.config import get_settings
import os
class BaseController:
    def __init__(self):
        
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_dir = os.path.join(self.base_dir,"assets/files")
        self.database_dir = os.path.join(self.base_dir,"assets/database")
    
    def generate_random_string(self, length=12):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    
    def get_database_path(self,db_name):
        full_path = os.path.join(
            self.database_dir,
            db_name
        )
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        return full_path
    