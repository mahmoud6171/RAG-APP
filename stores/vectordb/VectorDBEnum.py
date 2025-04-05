from enum import Enum


class VectorDBEnum(Enum):
    """
    Enum class for VectorDB types.
    """
    FAISS = "faiss"
    QDRANT = "qdrant"
    
    
class DistanceMethodEnum(Enum):
    """
    Enum class for distance methods.
    """
    COSINE = "cosine"
    DOT = "dot"

