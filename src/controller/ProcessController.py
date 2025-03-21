from .BaseController import BaseController
from .ProjectController import ProjectController
from langchain_community.document_loaders import TextLoader,PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessEnum
import os

class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id)
        
    def get_exn(self, project_id: str):
        return os.path.splitext(project_id)[-1]
    
    def get_fileLoader(self, file_id: str):
        
        ext = self.get_exn(file_id)
        file_path = os.path.join( self.project_path, file_id)
        if ext == ProcessEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        if ext == ProcessEnum.TXT.value:
            return TextLoader(file_path)
        return None

    
    def get_file_content(self, file_id: str):
        file_loader = self.get_fileLoader(file_id)
        if file_loader is None:
            return None
        return file_loader.load()
    
    def process_file_content(self, file_content: list, file_id: str,
                            chunk_size: int=100, overlap_size: int=20):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )
        
        file_content_texts = [rec.page_content for rec in file_content]
        file_content_metadata = [rec.metadata for rec in file_content]
        
        chunks = splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata)
        
        return chunks