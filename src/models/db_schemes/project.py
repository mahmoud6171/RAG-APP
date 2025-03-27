from pydantic import BaseModel, Field 
from typing import List, Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    _id : Optional[ObjectId]
    project_id :str = Field(...,min_length=1)
    
    @validator("project_id")
    def project_id_validator(cls, value):
        if not value.isalnum():
            raise ValueError("Project ID must be alphanumeric")
        return value
    
    class Config:
        arbitrary_types_allowed = True
        # json_encoders = {
        #     ObjectId: str
        # }