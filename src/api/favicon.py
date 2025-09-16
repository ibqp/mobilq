from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/favicon.ico")
async def favicon():
    path = 'mobilq/static/favicon.ico'
    return FileResponse(path)
