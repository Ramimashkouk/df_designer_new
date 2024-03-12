import aiofiles
import asyncio

from app.core.logger_config import get_logger

logger = get_logger(__name__)

class Process:
    def __init__(self):
        self.process = None
        self.pid = None

    async def start(self, cmd_to_run):
        async with aiofiles.open("process_io.log", "a", encoding="UTF-8") as file:
            self.process = await asyncio.create_subprocess_exec(
                *cmd_to_run.split(),
                stdout=file.fileno(),
                stderr=file.fileno(),
            )
            self.pid = self.process.pid  # Store the PID

    def check_status(self):
        """Check the status of the process."""
        if self.process is None:
            return "No process"
        elif self.process.returncode is None:
            return "Running"
        else:
            return f"Exited with return code {self.process.returncode}"

    def stop(self):
        if self.process:  # Check if a process has been started
            print(type(self.process), self.pid)
            try:
                self.process.terminate()  # Terminate the process
            except ProcessLookupError:
                print(f"Process {self.pid} not found. It may have already exited.")
