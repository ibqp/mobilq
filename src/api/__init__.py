from fastapi import APIRouter
from src.api.web import router as web_router
from src.api.elisa import router as elisa_router
from src.api.tele2 import router as tele2_router
from src.api.telia import router as telia_router

# Root router
root_router = APIRouter()

# Web routes
root_router.include_router(web_router)

# API routes
root_router.include_router(elisa_router)
root_router.include_router(tele2_router)
root_router.include_router(telia_router)
