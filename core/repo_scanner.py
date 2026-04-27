from pathlib import Path

from config.commands import WORKSPACE_DIR


def find_git_repositories():
    workspace = Path(WORKSPACE_DIR)

    if not workspace.exists():
        return []

    repos = []

    for item in workspace.iterdir():
        if item.is_dir() and (item / ".git").exists():
            repos.append(item)

    return sorted(repos, key=lambda path: path.name.lower())