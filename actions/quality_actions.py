from config.commands import COMMANDS
from core.command_executor import launch_command


def open_downloads():
    launch_command(COMMANDS["downloads_folder"])
    return "Downloads folder opened"


def open_desktop_index():
    launch_command(COMMANDS["desktop_index_folder"])
    return "DesktopIndex folder opened"