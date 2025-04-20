from typing import Dict, List
from ..VectorDBInterface import VectorDBInterface
from qdrant_client import QdrantClient,models
from ..VectorDBEnum import VectorDBEnum, DistanceMethodEnum
from models.db_schemes import RetrivedDocument
import logging

class QdrantDB(VectorDBInterface):
    """
    QdrantDB class for interacting with Qdrant vector database.
    """

    def __init__(self, db_path:str, distance_method: str):
        """
        Initialize the QdrantDB instance.
        """
        self.client = None
        self.distance_method = None
        self.db_path = db_path
        
        if distance_method == DistanceMethodEnum.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnum.DOT.value:
            self.distance_method = models.Distance.DOT
        
        self.logger = logging.getLogger(__name__)
        
    def connect(self):
        """
        Connect to the Qdrant database.
        """
        self.client = QdrantClient(path=self.db_path)
        self.logger.info("Connected to Qdrant database.")
        
        
    def disconnect(self):
        """
        Disconnect from the Qdrant database.
        """
        self.client = None
        self.logger.info("Disconnected from Qdrant database.")
            
    
    def is_collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name)
    
    def list_all_collections(self) -> List:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name)
    
    def delete_collection(self, collection_name: str) :
         if self.client.collection_exists(collection_name):
           return self.client.delete_collection(collection_name)
        
    def create_collection(self, collection_name: str,
                          embedding_dimension: int,
                          do_reset:bool =False) -> bool:
        if do_reset:
            _ = self.delete_collection(collection_name)

        if not self.is_collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_dimension,
                    distance=self.distance_method
                ),
            )
            self.logger.info(f"Collection {collection_name} created.")
            return True
        
        return False
    
    def insert_one(self, collection_name:str, text: str,metadata: dict,
                   embedding_text: List[float], record_id : str =None) :
        
        if self.client.is_collection_exists(collection_name):
            self.logger.info(f"Collection {collection_name} exists.")
            return None
        
        
        try:
            self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=[record_id],
                        vector=embedding_text,
                        payload={
                            "text": text, "metadata": metadata
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error inserting record: {e}")
            return False
        
        return True
    
    def insert_many(self, collection_name:str, texts: List[str],metadatas: List[dict],embedding_texts: List[List[float]],
                    record_ids: List[str] =None, batch_size :int =50):
        
        if metadatas is None:
            metadatas = [None] * len(texts)
        if record_ids is None:
            record_ids = list(0,len(texts))
            
        for i in range(0, len(texts), batch_size):
            end_batch = i+batch_size
            
            batch_texts = texts[i:end_batch]
            batch_metadatas = metadatas[i:end_batch]
            batch_embeddings = embedding_texts[i:end_batch]
            batch_record_ids = record_ids[i:end_batch]
            
            try:
                _ = self.client.upload_records(
                    collection_name=collection_name,
                    records=  [
                    models.Record(
                        id=batch_record_ids[x],
                        vector=batch_embeddings[x],
                        payload={
                            "text": batch_texts[x], "metadata": batch_metadatas[x]
                        }
                    )

                 for x in range(len(batch_texts))
            ])
            except Exception as e:
                self.logger.error(f"Error inserting batch: {e}")
                return False
            
            
        return True
    
    
    def serch_by_vector(self, collection_name: str, vector: List[float], top_k: int = 5) -> List[Dict]:
        if not self.is_collection_exists(collection_name):
            self.logger.error(f"Collection {collection_name} does not exist.")
            return []
        
        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=top_k,
            )
        except Exception as e:
            self.logger.error(f"Error searching by vector: {e}")
            return []
        
        return [
                RetrivedDocument(**{
                    "score":record.score,
                    "text":record.payload["text"]
                })
                for record in results
                ]