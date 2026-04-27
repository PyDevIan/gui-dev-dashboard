from config.commands import COMMANDS
from core.command_executor import run_command


def check_python_processes():
    output = run_command(COMMANDS["python_processes"])
    return output or "No Python processes running"


def check_node_processes():
    output = run_command(COMMANDS["node_processes"])
    return output or "No Node.js processes running"


def check_sql_services():
    output = run_command(COMMANDS["sql_services"])
    return output or "No SQL services found"