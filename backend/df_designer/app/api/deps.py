from app.clients.process_manager import ProcessManager

process_manager = ProcessManager()
def get_process_manager() -> ProcessManager:
    return process_manager
