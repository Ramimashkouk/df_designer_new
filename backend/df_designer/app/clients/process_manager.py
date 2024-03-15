import asyncio
from fastapi import WebSocket

from app.core.logger_config import get_logger
from app import Process

logger = get_logger(__name__)

class ProcessManager:
    def __init__(self):
        self.processes = {}

    async def start(self, cmd_to_run):
        process = Process()
        await process.start(cmd_to_run)
        self.processes[process.pid] = process

    def get_last_id(self):
        """Get the process_id of the last started process"""
        return list(self.processes.keys())[-1]

    def stop(self, pid):
        if pid in self.processes:
            self.processes[pid].stop()
