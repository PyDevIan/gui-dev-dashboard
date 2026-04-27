from actions.git_actions import get_selected_repo
from core.command_executor import launch_command
from state import app_state
from config.commands import CONDA_ACTIVATE_BAT
import tempfile
import uuid
from pathlib import Path

def get_selected_env():
    if not app_state.selected_conda_env:
        raise ValueError("No Conda environment selected")

    return app_state.selected_conda_env


def launch_in_repo_with_env(command_to_run):
    repo_path = get_selected_repo()
    env_name = get_selected_env()

    bat_path = Path(tempfile.gettempdir()) / f"dev_panel_{uuid.uuid4().hex}.bat"

    bat_content = f"""@echo off
echo Starting launcher...
echo Repo: {repo_path}
echo Env: {env_name}

CALL "{CONDA_ACTIVATE_BAT}" {env_name}
cd /d "{repo_path}"
{command_to_run}

pause
"""

    bat_path.write_text(bat_content, encoding="utf-8")

    launch_command(f'start "" cmd /k "{bat_path}"')

    return repo_path, env_name

def run_streamlit_app():
    repo_path, env_name = launch_in_repo_with_env("streamlit run app.py")
    return f"Streamlit launched in {repo_path.name} using env {env_name}"


def run_uvicorn_app():
    repo_path, env_name = launch_in_repo_with_env("uvicorn main:app --host 0.0.0.0 --port 8095 --reload")
    return f"Uvicorn launched in {repo_path.name} using env {env_name}"


def run_python_main():
    repo_path, env_name = launch_in_repo_with_env("python main.py")
    return f"python main.py launched in {repo_path.name} using env {env_name}"

def open_repo_terminal_with_env():
    repo_path, env_name = launch_in_repo_with_env("echo Environment ready.")

    return f"Terminal opened in {repo_path.name} using env {env_name}"