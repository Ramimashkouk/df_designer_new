from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.schemas.preset import Preset
from app.core.logger_config import get_logger
from app import Process

router = APIRouter()

logger = get_logger(__name__)

build_process = Process()

@router.post("/build/start", status_code=200) #TODO: shouldn't it be 201?
async def start_build(preset: Preset, background_tasks: BackgroundTasks): #TODO: add restirct
    global build_process
    await build_process.start(f"dflowd build_bot --preset {preset.body}")
    background_tasks.add_task(build_process.check_status)
    return {"status": "ok", "process_id":str(build_process.process.pid)}


@router.get("/build/stop", status_code=200)
async def stop_build():
    """Stop a build."""
    global build_process
    if build_process.process is not None:
        build_process.stop()
    else:
        raise HTTPException(status_code=400, detail="build/stop endpoint was requested before build/start")
    return {"status": "ok"}
