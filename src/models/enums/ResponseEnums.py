from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    FILE_PROCESS_SUCCESS = "file_process_success"
    FILE_PROCESS_FAILED = "file_process_failed"
    NO_FILE_PROVIDED = "no_file_provided"
    FILE_ID_ERRORS = "no_file_found_with_file_id"
    PROJECT_NOT_FOUND_ERROR = "project_not_found_error"
    INSER_INTO_VECTORDB_ERROR = "inset_into_vectordb_error"
    INSER_INTO_VECTORDB_SUCCESS = "insert_into_vectordb_sucess"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb_collection_retrieved"
    VECTORDB_SEARCH_ERROR = "vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS = "vectordb_search_success"
    RAG_ANSWER_ERROR = "rag_answer_error"
    RAG_ANSWER_SUCCESS = "rag_answer_success"