import asyncio
import json
import os
import subprocess
import typer
import uvicorn

from app.core.config import settings


cli = typer.Typer()

@cli.command("build_bot")
def build_bot(
    project_dir: str = settings.WORK_DIRECTORY,
    preset: str = "success"
):
    presets_build_path = os.path.join(project_dir, "df_designer", "presets", "build.json")
    with open(presets_build_path) as file:
        presets_build_file = json.load(file)

    if preset in presets_build_file:
        command_to_run = presets_build_file[preset]["cmd"]
        print(f"Running command for preset '{preset}': {command_to_run}")

        try:
            subprocess.run(command_to_run, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            # TODO: inform ui
    else:
        print(f"Preset '{preset}' not found in build.json.")


#### TODO: move to DB DIR
# def setup_database(project_dir: str) -> None:
#     """Set up the database."""
#     engine = create_engine(f"sqlite:///{project_dir}/{app.database_file}")
#     Base.metadata.create_all(engine)


def _setup_backend(ip_address: str, port: int, dir_logs: str, cmd_to_run: str, conf_reload: str, project_dir: str) -> None:
    """Set up the application configurations."""
    # settings.cmd_to_run = cmd_to_run
    # settings.dir_logs = dir_logs
    settings.WORK_DIRECTORY = project_dir # TODO: set a function for setting the value
    # setup_database(project_dir)
    settings.setup_server(ip_address, port, conf_reload, project_dir)


async def _run_server() -> None:
    """Run the server."""
    await settings.server.run()


@cli.command("run_backend")
def run_backend(
    ip_address: str = settings.HOST,
    port: int = settings.BACKEND_PORT,
    dir_logs: str = settings.DIR_LOGS,
    cmd_to_run: str = settings.CMD_TO_RUN,
    conf_reload: str = str(settings.CONF_RELOAD),
    project_dir: str = settings.WORK_DIRECTORY,
) -> None:
    """Run the backend."""
    _setup_backend(ip_address, port, dir_logs, cmd_to_run, conf_reload, project_dir)
    settings.server.run()
