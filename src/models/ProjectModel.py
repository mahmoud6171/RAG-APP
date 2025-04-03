from .BaseDataModel import BaseDataModel
from .db_schemes.project import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
        
   
    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance
  
   
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indicies = Project.get_indicies()
            for index in indicies:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                    )

    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project.id = result.inserted_id
        return project
    
    
    async def get_project_or_create_one(self,project_id: str):
        #check if project already exists
        # print(f"Before find_one: {type(self.collection)}")
        # print(f"Has find_one: {'find_one' in dir(self.collection)}")
        record = await self.collection.find_one({
            "project_id": project_id
        })
        
        if record is None:
            project = Project(project_id=project_id)
            project = await self.create_project(project)
            return project
        
        return Project(**record)
    
    async def get_all_projects(self, page_size: int=10, page_number: int=1):
        #count total number of documents
        total = await self.collection.count_documents({})
        #calculate number of pages
        total_pages = total // page_size 
        if total % page_size > 0:
            total_pages += 1
        #get all documents
        cursor = self.collection.find({}).limit(page_size).skip(page_size*(page_number-1))
        projects = []
        async for project in cursor:
            projects.append(Project(**project))
        return projects, total_pages
        
        # cursor = self.collection.find({})
        # projects = await cursor.to_list(length=page_size,skip=page_size*page_number)
        # return [Project(**project) for project in projects]
        
    