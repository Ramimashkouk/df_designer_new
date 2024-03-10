from pydantic_settings import BaseSettings
import uvicorn

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    WORK_DIRECTORY: str = "."

    # consult about the namings
    APP: str = "app.main:app" 
    HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000
    UI_PORT: int = 3000
    LOG_LEVEL: str = "info"
    CONF_RELOAD: bool = True
    DIR_LOGS: str = "logs"   ### Ensure this's needed
    # database_file = "database.sqlite"
    CMD_TO_RUN: str = ""    ### Ensure this's needed
    server: uvicorn.Server = uvicorn.Server(
        uvicorn.Config(APP, HOST, BACKEND_PORT, LOG_LEVEL, CONF_RELOAD, WORK_DIRECTORY)
    )
    
    def setup_server(self, ip_address: str, port: int, conf_reload: str, project_dir: str) -> None:
        """Set up the server."""
        config = uvicorn.Config(
            app=self.APP,
            host=ip_address,
            port=port,
            log_level=self.LOG_LEVEL,
            reload=conf_reload.lower() in ["true", "yes", "t", "y", "1"],
            reload_dirs=project_dir
        )
        self.server = uvicorn.Server(config)

settings = Settings()
