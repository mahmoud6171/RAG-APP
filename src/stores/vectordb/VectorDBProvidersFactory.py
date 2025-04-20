from .providers import QdrantDB
from .VectorDBEnum import VectorDBEnum
from controller.BaseController import BaseController


class VectorDBProviderFactory:
    """Factory class for creating vector database providers."""
    
    def __init__(self, config: dict):
        self.config = config
        self.basecontroller = BaseController()
    
    
    def create_provider(self,provider_type: str):
        """Creates a vector database provider based on the provider type."""
        if provider_type == VectorDBEnum.QDRANT.value:
            db_path = self.basecontroller.get_database_path(self.config.VECTOR_DB_PATH)
            return QdrantDB(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METRIC,
                
            )
            
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")