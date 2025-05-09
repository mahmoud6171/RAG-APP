from fastapi import  APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from Routes.schemes.nlp import PushRequset,SearchRequest
from models.enums import ResponseSignal
from models import ProjectModel,ChunkModel
from controller import NLPController

import logging

logger = logging.getLogger("uvicorn.error")

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags= ["api_v1","nlp"]
)

@nlp_router.post("/index/push/{project_id}")
async def index_project(request : Request, push_request : PushRequset, project_id : str):
    
    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )
    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )
    nlp_controller =  NLPController(
        verctordb_clinet=request.app.verctordb_clinet,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
    )
    
    project = await project_model.get_project_or_create_one(project_id = project_id)
    
    if not project :
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSignal.PROJECT_NOT_FOUND_ERROR.value}
        )
    
    page_no =1
    inserted_item_count = 0
    ids=0
    has_records= True
    
    while has_records:
        page_chunk = await chunk_model.get_project_chunk(project_id = project.id,page_no=page_no)
        if len(page_chunk):
            page_no
        
        if len(page_chunk)==0 or not page_chunk:
            has_records = False
            break
        
        
        chunk_ids = list(range(ids, ids+len(page_chunk)))
        ids+=len(page_chunk)
        
        is_inserted = nlp_controller.index_to_vectorDB(
            project = project,
            chunks = page_chunk,
            do_reset = push_request.do_reset,
            chunk_ids=chunk_ids
        )

        if not is_inserted :
            return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSignal.INSER_INTO_VECTORDB_ERROR.value}
            )
        
        inserted_item_count +=len(page_chunk)
        
    return  JSONResponse(
         content={
             "signal": ResponseSignal.INSER_INTO_VECTORDB_SUCCESS.value,
             "inserted item count":inserted_item_count
             }
    )
            
@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: str):
    
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    nlp_controller =  NLPController(
        verctordb_clinet=request.app.verctordb_clinet,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
    )

    collection_info = nlp_controller.get_vectordb_info(project=project)

    return JSONResponse(
        content={
            "signal": ResponseSignal.VECTORDB_COLLECTION_RETRIEVED.value,
            "collection_info": collection_info
        }
    )

@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request, project_id: str, search_request: SearchRequest):
    
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPController(
        verctordb_clinet=request.app.verctordb_clinet,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    results = nlp_controller.search_vector_db_collection(
        project=project, text=search_request.text, limit=search_request.limit
    )

    if not results:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.VECTORDB_SEARCH_ERROR.value
                }
            )
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.VECTORDB_SEARCH_SUCCESS.value,
            "results": [ result.dict()  for result in results ]
        }
    )

@nlp_router.post("/index/answer/{project_id}")
async def answer_rag(request: Request, project_id: str, search_request: SearchRequest):
    
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPController(
        verctordb_clinet=request.app.verctordb_clinet,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    answer, full_prompt, chat_history = nlp_controller.answer_rag_question(
        project=project,
        query=search_request.text,
        limit=search_request.limit,
    )

    if not answer:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.RAG_ANSWER_ERROR.value
                }
        )
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.RAG_ANSWER_SUCCESS.value,
            "answer": answer,
            "full_prompt": full_prompt,
            "chat_history": chat_history
        }
    )