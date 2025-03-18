from fastapi import FastAPI
from Routes import base

app = FastAPI()
app.include_router(base.base_router)


