from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import   UploadFile
from models import ResponseSignal
import re
import os
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        
       
    def validate_uplaod_data(self, uploaded_file: UploadFile):
        
        if uploaded_file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if uploaded_file.size > (self.app_settings.FILE_MAX_SIZE *102465):
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    def generate_unique_file_path(self,orig_file_name, project_id):
        random_file_name = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id)
        
        cleaned_file_name = self.get_clean_file_name(orig_file_name)
        
        new_file_name = os.path.join(project_path, f"{random_file_name}_{cleaned_file_name}")
        
        while os.path.exists(new_file_name):
            random_file_name = self.generate_random_string()
            new_file_name = os.path.join(project_path, f"{random_file_name}_{cleaned_file_name}")
        
        return new_file_name, f"{random_file_name}_{cleaned_file_name}"
        
        
    def get_clean_file_name(self, file_name):
        cleaned_file_name = re.sub(r'[^\w.]+', '', file_name.strip())
        cleaned_file_name.replace(" ", "_")
        return cleaned_file_name
        