from pathlib import Path

from core.command_executor import launch_command


def open_folder_path(path_text):
    path = Path(path_text.strip())

    if not path_text.strip():
        raise ValueError("No folder path provided")

    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a folder: {path}")

    launch_command(f'explorer "{path}"')
    return f"Opened folder: {path}"