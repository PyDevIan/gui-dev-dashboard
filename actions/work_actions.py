import webbrowser

from config.commands import COMMANDS
from core.command_executor import launch_command


def open_vs_insiders():
    launch_command(COMMANDS["vs_insiders"])
    return "Visual Studio Code Insiders launched successfully"


def open_ssms_22():
    launch_command(COMMANDS["ssms_22"])
    return "SQL Server Management Studio 22 launched successfully"

def open_comet_browser():
    launch_command(COMMANDS["open_comet"])
    return "Comet Launched Successfully"

def open_jira_tickets():
    webbrowser.open(COMMANDS["jira_tickets_url"])
    return "Jira tickets opened successfully"

def open_codex():
    webbrowser.open(COMMANDS["chat_gpt_codex"])
    return "Codex Initiated"

def open_github():
    webbrowser.open(COMMANDS["github_url"])
    return "GitHub Initiated"

def open_openprj():
    webbrowser.open(COMMANDS["open_project_url"])
    return "Project Management Mode Enabled"

def open_dbdiagram():
    webbrowser.open(COMMANDS["oprn_dbdiagram"])
    return "Data Engineering Software Initiated"

def open_kpidash():
    webbrowser.open(COMMANDS['kpi_dashboard'])
    return "KPI DashBoard Launched"
