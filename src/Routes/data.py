from fastapi import  APIRouter, Depends, UploadFile, status
from controller import DataController, ProjectController
from fastapi.responses import JSONResponse
from helpers.config import get_settings
from models import ResponseSignal
import aiofiles
import os
import logging

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags= ["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id:str, file : UploadFile, app_settings= Depends(get_settings)):
    
     
    data_controller = DataController()
    vaild, result_signal = data_controller.validate_uplaod_data(uploaded_file= file)
    
    if not vaild:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": result_signal}
            )
        
    project_dir = ProjectController().get_project_path(project_id)
    
    file_path = data_controller.generate_unique_file_name(
        orig_file_name=file.filename,
        project_id=project_dir)
   
    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await buffer.write(chunk)
    except Exception as e:
        logger.error(f"An error occurred while uploading the file: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": ResponseSignal.FILE_UPLOAD_FAILED.value}
        )
    
    return JSONResponse(
        content={"message": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                 "file_size": file.size,
                 "file_name": file.filename,
                 "file_path": file_path}
        )