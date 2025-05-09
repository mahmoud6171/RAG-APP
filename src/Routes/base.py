from fastapi import FastAPI, APIRouter, Depends
from helpers.config import get_settings
import os


base_router = APIRouter(
    prefix="/api/v1",
    tags= ["api_v1"]
)

@base_router.get("/")
async def welcome(app_settings= Depends(get_settings)):
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {"message": f"Welcome to the {app_name}! Version: {app_version}"}