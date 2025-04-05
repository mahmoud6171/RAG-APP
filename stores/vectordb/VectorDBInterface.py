from abc import ABC, abstractmethod
from typing import List, Dict


class VectorDBInterface(ABC):
    """
    Abstract base class for vector databases.
    """

    @abstractmethod
    def connect( self):
        """
        Connect to the vector database.
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """
        Disconnect from the vector database.
        """
        pass
    
    
    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists in the database.

        :param collection_name: The name of the collection.
        :return: True if the collection exists, False otherwise.
        """
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        """
        Get information about a collection.

        :param collection_name: The name of the collection.
        :return: A dictionary containing collection information.
        """
        pass
    
    
    @abstractmethod
    def create_collection(self, collection_name: str, embedding_dimension: int, do_reset:bool =False) -> bool:
        """
        Create a new collection in the database.

        :param collection_name: The name of the collection.
        :param embedding_dimension: The dimension of the embeddings.
        :return: True if the collection was created successfully, False otherwise.
        """
        pass
    
    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection from the database.

        :param collection_name: The name of the collection.
        :return: True if the collection was deleted successfully, False otherwise.
        """
        pass
    
    @abstractmethod
    def list_all_collections(self) -> List:
        """
        List all collections in the database.

        :return: A list of collection names.
        """
        pass
    
    @abstractmethod
    def insert_one(self, collection_name:str, text: str,metadata: dict,
                   embedding_text: List[float], record_id : str =None) :
        """
        Insert a single document into the collection.

        :param collection_name: The name of the collection.
        :param text: The text of the document.
        :param metadata: Metadata associated with the document.
        :param embedding: The embedding of the document.
        :return: True if the document was inserted successfully, False otherwise.
        """
        pass
    
    @abstractmethod
    def insert_many(self, collection_name:str, texts: List[str],metadatas: List[dict],embedding_texts: List[List[float]],
                    record_ids: List[str] =None, batch_size :int =50):
        """
        Insert multiple documents into the collection.

        :param collection_name: The name of the collection.
        :param texts: A list of texts.
        :param metadatas: A list of metadata dictionaries.
        :param embedding_texts: A list of embeddings.
        :return: True if the documents were inserted successfully, False otherwise.
        """
        pass
    
    @abstractmethod
    def serch_by_vector(self, collection_name: str, vector: List[float], top_k: int = 5) -> List[Dict]:
        """
        Search for similar documents based on a vector.

        :param collection_name: The name of the collection.
        :param vector: The query vector.
        :param top_k: The number of top results to return.
        :return: A list of dictionaries containing the search results.
        """
        pass