from pathlib import Path

from config.commands import COMMANDS
from core.command_executor import launch_command
from state import app_state


def open_vscode():
    if app_state.selected_repo_path:
        repo_path = Path(app_state.selected_repo_path)

        if repo_path.exists() and repo_path.is_dir():
            launch_command(f'code "{repo_path}"')
            return f"VS Code opened: {repo_path.name}"

    launch_command(COMMANDS["vscode"])
    return "VS Code launched successfully"


def open_terminal():
    launch_command(COMMANDS["terminal"])
    return "PowerShell launched successfully"


def open_project_folder():
    launch_command(COMMANDS["project_folder"])
    return "Project folder opened successfully"


def open_ai_dept():
    launch_command(COMMANDS["open_AI_dept"])
    return "AI Dept folder opened successfully"

def open_copilot_codex():
    launch_command(COMMANDS["codex"])
    return "Codex Copilot Ready for Duty"