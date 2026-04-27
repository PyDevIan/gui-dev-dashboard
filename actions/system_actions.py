from config.commands import COMMANDS
from core.command_executor import run_command, launch_command


def open_logs_file():
    launch_command(COMMANDS["logs_file"])
    return "Logs file opened successfully"


def open_task_manager():
    launch_command(COMMANDS["task_manager"])
    return "Task Manager launched successfully"


def check_python_version():
    output = run_command(COMMANDS["python_version"])
    return f"Python version: {output}"