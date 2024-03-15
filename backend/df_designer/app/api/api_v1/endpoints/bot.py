import asyncio
from fastapi import APIRouter, HTTPException, Depends, WebSocket, Query

from app.schemas.preset import Preset
from app.core.logger_config import get_logger
from app.clients.process_manager import ProcessManager
from app.api import deps
from app.clients.websocket_manager import WebSocketManager


router = APIRouter()

logger = get_logger(__name__)


@router.post("/build/start", status_code=201)
async def start_build(preset: Preset, process_manager: ProcessManager = Depends(deps.get_process_manager)):
    await process_manager.start(f"dflowd build_bot --preset {preset.body}")
    pid = process_manager.get_last_id()
    return {"status": "ok", "pid": pid}


@router.get("/build/stop/{pid}", status_code=200)
async def stop_build(pid: int, process_manager: ProcessManager = Depends(deps.get_process_manager)):
    if pid not in process_manager.processes:
        raise HTTPException(status_code=404, detail="Process not found")
    process_manager.stop(pid)
    return {"status": "ok"}


@router.get("/build/status/{pid}", status_code=200)
async def check_build_status(pid: int, process_manager: ProcessManager = Depends(deps.get_process_manager)):
    if pid not in process_manager.processes:
        raise HTTPException(status_code=404, detail="Process not found")
    status = process_manager.processes[pid].check_status()
    return {"status": status}


@router.websocket("/run/start")
async def start_run(
    websocket: WebSocket,
    websocket_manager: WebSocketManager = Depends(deps.get_websocket_manager),
    process_manager: ProcessManager = Depends(deps.get_process_manager),
):
    await websocket_manager.start(websocket, process_manager)

    output_task = asyncio.create_task(websocket_manager.send_process_output_to_websocket(process_manager))
    input_task = asyncio.create_task(websocket_manager.forward_websocket_messages_to_process(process_manager))

    # Wait for either task to finish
    _, pending = await asyncio.wait(
        [output_task, input_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    await websocket_manager.stop(process_manager, pending)


@router.get("/run/stop", status_code=200)
async def stop_run(websocket_manager: WebSocketManager = Depends(deps.get_websocket_manager), process_manager: ProcessManager = Depends(deps.get_process_manager)):
    if websocket_manager.websocket is None:
        raise HTTPException(status_code=404, detail="Process not found")
    await websocket_manager.stop(process_manager = process_manager)
    return {"status": "ok"}


@router.get("/run/status", status_code=200)
async def check_run_status(websocket_manager: WebSocketManager = Depends(deps.get_websocket_manager), process_manager: ProcessManager = Depends(deps.get_process_manager)):
    if websocket_manager.pid not in process_manager.processes:
        raise HTTPException(status_code=404, detail="Process not found")
    status = websocket_manager.check_status(process_manager)
    return {"status": status}
