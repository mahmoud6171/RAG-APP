from fastapi import FastAPI
from Routes import base,data,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
from stores.llm import LLMProviderFactory
from stores.vectordb.VectorDBProvidersFactory import VectorDBProviderFactory
# Ensure the correct path to Template_Parser is used
from stores.llm.templates.templates_parser import Template_Parser


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(settings)
    
    app.generation_client = llm_provider_factory.create_provider(provider_type=settings.GENERTION_BACKEND)
    app.generation_client.set_generation_model(settings.GENERATION_MODEL_ID)
    
    app.embedding_client = llm_provider_factory.create_provider(provider_type = settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id = settings.EMBEDDING_MODEL_ID, embedding_size = settings.EMBEDDING_MODEL_SIZE)
    
    app.verctordb_clinet = vectordb_provider_factory.create_provider(
        provider_type = settings.VECTOR_DB_BACKEND
    )
    app.verctordb_clinet.connect()
    
    app.template_parser = Template_Parser(
        language = settings.DEFAULT_LANGUAGE
    )
    
    
    
    yield
    app.mongo_conn.close()
    app.verctordb_clinet.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)



