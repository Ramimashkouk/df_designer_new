from app import Process

class ProcessManager:
    def __init__(self):
        self.processes = {}

    async def start(self, cmd_to_run):
        process = Process()
        await process.start(cmd_to_run)
        self.processes[process.pid] = process  # Use the PID as the key

    def stop(self, pid):
        if pid in self.processes:
            self.processes[pid].stop()
            # del self.processes[pid]  # Remove the process from the dictionary
