from .BaseDataModel import BaseDataModel
from models.enums.DataBaseEnum import DataBaseEnum
from .db_schemes.data_chunk import DataChunk
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]


    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance
  
   
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
            indicies = DataChunk.get_indicies()
            for index in indicies:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                    )

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        chunk.id = result.inserted_id
        return chunk
    
    async def get_chunk(self, chunk_id: str):
        record = await self.collection.find_one({
            "_id":ObjectId(chunk_id)
        })
        if record is None:
            return None
        return DataChunk(**record)
    
    async def insert_many_chunks(self, chunks: list, batch_size: int =100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            requests = [InsertOne(chunk.dict(by_alias=True, exclude_unset=True)) for chunk in batch]
            result = await self.collection.bulk_write(requests)
            print(f"Inserted {result.inserted_count} chunks")
            
        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })
        return result.deleted_count 