from fastapi import FastAPI, APIRouter, Depends, UploadFile
from helpers.config import get_setting
import os


data_router = APIRouter(
    prefix="/api/v1/data",
    tags= ["api_v1","data"]
)

@data_router.post("upload/{project_id}")
async def upload_file(project_id:str, file : UploadFile, app_settings= Depends(get_setting)):
    
    app_name = app_settings.APP_Name
    app_version = app_settings.APP_Version 
    pass 