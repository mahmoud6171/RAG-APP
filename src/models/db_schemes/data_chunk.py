from pydantic import BaseModel, Field 
from typing import List, Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    _id : Optional[ObjectId]
    chunk_text : str = Field(...,min_length=1)
    chunk_metadata : dict 
    chunk_order : int = Field(...,gt=0)
    project_id : ObjectId
    
    @validator("project_id")
    def project_id_validator(cls, value):
        if not value.isalnum():
            raise ValueError("Project ID must be alphanumeric")
        return value
    
    
    
    class Config:
        arbitrary_types_allowed = True
       