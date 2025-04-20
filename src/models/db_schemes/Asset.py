from pydantic import BaseModel, Field, field_validator 
from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime,timezone

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id :ObjectId
    asset_name : str = Field(...,min_length=1)
    asset_type : str = Field(...,min_length=1)
    asset_metadata : dict = Field(default=None)
    asset_size : int = Field(...,gt=0)  
    asset_pushed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    
    
    class Config:
        arbitrary_types_allowed = True
    
    @classmethod
    def get_indicies(cls):
    
        return [
            {
                "key": [("asset_project_id", 1)],
                "name": "asset_project_id_index_1",
                "unique": False,
            },
             {
                "key": [("asset_project_id", 1),
                        ("asset_name", 1)],
                "name": "asset_project_id_name_index_1",
                "unique": True,
            },
        ]