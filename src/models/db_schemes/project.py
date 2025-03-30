from pydantic import BaseModel, Field, field_validator 
from typing import List, Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id : Optional[ObjectId] = Field(None, alias="_id")
    project_id :str = Field(...,min_length=1)
    
    @field_validator("project_id")
    def project_id_validator(cls, value):
        if not value.isalnum():
            raise ValueError("Project ID must be alphanumeric")
        return value
    
    class Config:
        arbitrary_types_allowed = True
        
        
    @classmethod
    def get_indicies(cls):
    
        return [
            {
                "key": [("project_id", 1)],
                "name": "project_id_index_1",
                "unique": True,
            },
        ]