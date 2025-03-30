from fastapi import  APIRouter, Depends, UploadFile, status, Request
from controller import DataController, ProjectController,ProcessController
from models.ProjectModel import ProjectModel
from fastapi.responses import JSONResponse
from helpers.config import get_settings
from models.db_schemes.data_chunk import DataChunk
from models.ChunkModel import ChunkModel
from .schemes.data import ProcessRequest
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
async def upload_file(request: Request,project_id:str,
                      file : UploadFile, app_settings= Depends(get_settings)):
    
    project_model = await ProjectModel.create_instance(
       db_client = request.app.db_client
    )
    
    project = await project_model.get_project_or_create_one(project_id= project_id)
    
    data_controller = DataController()
    vaild, result_signal =  data_controller.validate_uplaod_data(uploaded_file= file)
    
    if not vaild:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": result_signal}
            )
        
    project_dir = ProjectController().get_project_path(project_id)
    
    file_path, file_id = data_controller.generate_unique_file_path(
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
                 "file_name": file.filename,
                 "file_id": file_id,
                 "project_id": str(project._id)
                 }
        )
    
@data_router.post("/process/{project_id}")
async def process_data(request :Request,project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size= process_request.chunk_size
    overlap_size= process_request.overlap_size
    do_reset = process_request.do_reset
    
    project_model = await ProjectModel.create_instance(
       db_client = request.app.db_client
    )
    
    project = await project_model.get_project_or_create_one(project_id= project_id)
    
    
    process_controller = ProcessController(project_id= project_id)
    file_content = process_controller.get_file_content(file_id)
    content_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size= chunk_size,
        overlap_size= overlap_size
    )
    
    if content_chunks is None or len(content_chunks) == 0: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSignal.FILE_PROCESS_FAILED.value}
        )
        
    #save chunks to db
    file_chunks_model = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i + 1,
            chunk_project_id=project.id,
        )
        for i, chunk in enumerate(content_chunks)
    ]
    
    chunk_model = await ChunkModel.create_instance(
       db_client = request.app.db_client
    )
    if do_reset:
        await chunk_model.delete_chunks_by_project_id(project_id=project.id)
    #delete old chunks
    #insert new chunks
    
    no_records = await chunk_model.insert_many_chunks(file_chunks_model)
    
    return JSONResponse(
            content={"message": ResponseSignal.FILE_PROCESS_SUCCESS.value,
                    "inserted_chunks": no_records
                 }
    )