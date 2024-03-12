from fastapi import APIRouter, HTTPException, Depends

from app.schemas.preset import Preset
from app.core.logger_config import get_logger
from app.clients.process_manager import ProcessManager
from app.api import deps


router = APIRouter()

logger = get_logger(__name__)


@router.post("/build/start", status_code=201)
async def start_build(preset: Preset, process_manager: ProcessManager = Depends(deps.get_process_manager)):
    await process_manager.start(f"dflowd build_bot --preset {preset.body}")
    pid = list(process_manager.processes.keys())[-1]  # Get the PID of the last started process
    return {"status": "ok", "pid": pid}

@router.get("/build/stop/{pid}", status_code=200)
async def stop_build(pid: int, process_manager: ProcessManager = Depends(deps.get_process_manager)):
    if pid not in process_manager.processes:
        raise HTTPException(status_code=404, detail="Process not found")
    process_manager.stop(pid)
    return {"status": "ok"}

@router.get("/build/status/{pid}", status_code=200)
async def check_status(pid: int, process_manager: ProcessManager = Depends(deps.get_process_manager)):
    if pid not in process_manager.processes:
        raise HTTPException(status_code=404, detail="Process not found")
    status = process_manager.processes[pid].check_status()
    return {"status": status}
