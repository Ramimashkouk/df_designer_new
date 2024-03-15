import asyncio
from asyncio.tasks import Task
from fastapi import WebSocket
from typing import Optional

from app.core.logger_config import get_logger
from app.clients.process_manager import ProcessManager

logger = get_logger(__name__)

class WebSocketManager:
    def __init__(self):
        self.websocket = None
        self.pid = None

    async def start(self, websocket: WebSocket, process_manager: ProcessManager): # TODO: why not intiate name?
        self.websocket = websocket
        await self.websocket.accept()

        preset = await self.websocket.receive_text()
        await process_manager.start(f"dflowd run_bot --preset {preset}")
        self.pid = process_manager.get_last_id()
        await self.websocket.send_text(": ".join(["Process_id", str(self.pid)]))

    async def stop(self, process_manager: ProcessManager, pending_tasks: Optional[set[Task[None]]]=None):
        # Cancel any pending tasks to avoid resource leaks
        if pending_tasks is not None and pending_tasks:
            for task in pending_tasks:
                task.cancel()

        if self.websocket is None:
            raise RuntimeError(f"Cannot stop a websocket '{self.pid}' that has not started yet.")
        # Ensure the subprocess is terminated
        process_manager.stop(self.pid)
        await process_manager.processes[self.pid].wait()

        await self.websocket.close()

    def check_status(self, process_manager: ProcessManager):
        return process_manager.processes[self.pid].check_status()

    async def send_process_output_to_websocket(self, process_manager: ProcessManager):
        """Read and forward process output to the websocket client.
        
        Args:
          pid: process_id, attribute of asyncio.subprocess.Process
        """
        while True:
            response = await process_manager.processes[self.pid].read_stdout()
            if not response:
                break
            await self.websocket.send_text(response.decode().strip())

    async def forward_websocket_messages_to_process(self, process_manager: ProcessManager):
        """Listen for messages from the websocket and send them to the subprocess.
        
        Args:
          pid: process_id, attribute of asyncio.subprocess.Process
        """
        try:
            while True:
                user_message = await self.websocket.receive_text()
                process_manager.processes[self.pid].write_stdin(user_message.encode() + b'\n')
        except asyncio.CancelledError:
            logger.info("Websocket connection is closed")
