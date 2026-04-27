from config.commands import COMMANDS
from core.command_executor import run_command


def show_docker_containers():
    output = run_command(COMMANDS["docker_ps"], timeout=30)
    return output or "No Docker containers running"