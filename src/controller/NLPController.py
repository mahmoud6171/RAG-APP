from .BaseController import BaseController
from models.db_schemes.project import Project
from models.db_schemes.data_chunk import DataChunk
from stores.llm.LLMEnums import DocumentTypeEnums
from typing import List
import logging
import os
import json
import httpx


class NLPController(BaseController):
    def __init__(self,verctordb_clinet, embedding_client,
                 generation_client,template_parser):
        super().__init__()
        
        self.verctordb_clinet = verctordb_clinet
        self.embedding_client = embedding_client
        self.generation_client = generation_client
        self.template_parser = template_parser
        
        self.logger = logging.getLogger("uvicorn.error")
        
    def create_collection_name(self, project_id :str):
        return f"collection_{project_id}".strip()
    
    def reset_vectordb_collection(self, project : Project):
        collection_name = self.create_collection_name(project_id= project.project_id)
        return self.verctordb_clinet.delete_collection(collection_name)
        
    
    def get_vectordb_info(self,project : Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.verctordb_clinet.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    
    def index_to_vectorDB(self,project :Project, chunks :List[DataChunk],
                          chunk_ids :List[int],do_reset = False):
        
        #step no.1 : get collection name
        collection_name = self.create_collection_name(project_id= project.project_id)
        
        #step no.2 : manage item
        texts = [rec.chunk_text for rec in chunks]
        metadatas = [rec.chunk_metadata   for rec in chunks]
        
        try:
            vectors = [
                self.embedding_client.generate_embedding(
                    text=text, document_type=DocumentTypeEnums.DOCUMENT.value
                )
                for text in texts
            ]
        except httpx.ConnectError as e:
            # Log the error and return a meaningful response
            self.logger.error(f"Failed to connect to embedding service: {e}")
            return {"error": "Failed to connect to embedding service"}
        
        #step no.3 : create collection if not exict
        _ = self.verctordb_clinet.create_collection(collection_name = collection_name,
                                                    embedding_dimension = self.embedding_client.embedding_size,
                                                    do_reset = do_reset)
        
        #step no.4 : insert into vectorDB
        _ = self.verctordb_clinet.insert_many(collection_name = collection_name, texts=texts,
                                              metadatas=metadatas,
                                              record_ids=chunk_ids,embedding_texts=vectors)
        
        return True
    
    
    def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):

        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: get text embedding vector
        try:
            vector = self.embedding_client.generate_embedding(
                text=text, document_type=DocumentTypeEnums.QUERY.value
            )
        except httpx.ConnectError as e:
            # Log the error and return a meaningful response
            self.logger.error(f"Failed to connect to embedding service: {e}")
            return {"error": "Failed to connect to embedding service"}

        if not vector or len(vector) == 0:
            return False

        # step3: do semantic search
        results = self.verctordb_clinet.serch_by_vector(
            collection_name=collection_name,
            vector=vector,
            top_k=limit
        )

        if not results:
            return False

        return results
    
    def answer_rag_question(self, project: Project, query: str, limit: int = 10):
        
        answer, full_prompt, chat_history = None, None, None

        # step1: retrieve related documents
        retrieved_documents = self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit,
        )

        if not retrieved_documents or len(retrieved_documents) == 0:
            return answer, full_prompt, chat_history
        
        # step2: Construct LLM prompt
        system_prompt = self.template_parser.get("rag", "system_prompt")

        documents_prompts = "\n".join([
            self.template_parser.get("rag", "document_prompt", {
                    "doc_num": idx + 1,
                    "chunk_text": doc.text,
            })
            for idx, doc in enumerate(retrieved_documents)
        ])

        footer_prompt = self.template_parser.get("rag", "footer_prompt")

        # step3: Construct Generation Client Prompts
        chat_history = [
            self.generation_client.constract_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]

        full_prompt = "\n\n".join([ documents_prompts,  footer_prompt])

        # step4: Retrieve the Answer
        answer = self.generation_client.generate_response(
            prompt=full_prompt,
            chat_history=chat_history
        )

        return answer, full_prompt, chat_history

