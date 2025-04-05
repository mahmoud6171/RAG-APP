from fastapi import FastAPI
from Routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
from ..stores.llm import LLMProviderFactory




@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    
    app.generation_client = LLMProviderFactory.create_provider(provider_type = settings.GENERTION_BACKEND)
    app.generation_client.set_generation_model(settings.GENERATION_MODEL)
    
    app.embedding_client = LLMProviderFactory.create_provider(provider_type = settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id = settings.EMBEDDING_MODEL_ID, embedding_size = settings.EMBEDDING_MODEL_SIZE)
    
    yield
    app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)



