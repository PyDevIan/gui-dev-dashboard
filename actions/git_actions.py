from pathlib import Path

from state import app_state
from core.command_executor import run_command


def get_selected_repo():
    if not app_state.selected_repo_path:
        raise ValueError("No Git repository selected")

    repo_path = Path(app_state.selected_repo_path)

    if not repo_path.exists():
        raise FileNotFoundError(f"Repo path does not exist: {repo_path}")

    if not (repo_path / ".git").exists():
        raise ValueError(f"Selected folder is not a Git repository: {repo_path}")

    return repo_path


def git_status():
    repo_path = get_selected_repo()
    output = run_command("git status --short", cwd=repo_path)
    return output or "Git working tree clean"


def git_branch():
    repo_path = get_selected_repo()
    output = run_command("git branch --show-current", cwd=repo_path)
    return f"Current branch: {output}"


def git_pull():
    repo_path = get_selected_repo()
    output = run_command("git pull", timeout=120, cwd=repo_path)
    return output or "Git pull completed"