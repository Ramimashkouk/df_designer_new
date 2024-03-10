from fastapi import APIRouter
from app.schemas.preset import Preset
from app.cli import build_bot
from app.core.config import settings

router = APIRouter()


@router.post("/builds/start", status_code=200) #TODO: shouldn't it be 201?
async def start_build(preset: Preset): #TODO: add restirct
    """Start a build."""
    build_bot(project_dir=settings.WORK_DIRECTORY, preset="failure")
    return preset
