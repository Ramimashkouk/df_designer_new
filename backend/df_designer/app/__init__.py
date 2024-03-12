import asyncio

from app.core.logger_config import get_logger

logger = get_logger(__name__)

class Process:
    def __init__(self):
        self.process = None

    async def start(self, cmd_to_run):
        logger.info("cmd_to_run: %s", cmd_to_run)
        self.process = await asyncio.create_subprocess_exec(
            *cmd_to_run.split(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    async def check_status(self):
        while True:
            await asyncio.sleep(1)
            if self.process.returncode is not None:
                if self.process.returncode == 0:
                    logger.info("Completed successfully yo")
                    break
                elif self.process.returncode > 0:
                    logger.error("Error yo")
                    break
            else:
                logger.info("process '{self.process.pid}' haven't completed yet")

    def stop(self):
        """Stop the process."""
        if self.process.returncode is None:
            self.process.terminate()
