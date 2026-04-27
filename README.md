# Developer Control Panel

A Python desktop control panel built with Tkinter and ttkbootstrap for launching development tools, opening work resources, monitoring processes, and managing local development workflows.

## Current Features

- Modern dark sci-fi dashboard UI with ttkbootstrap
- Sidebar navigation with active state
- Action registry grouped by category
- Scrollable quick actions area
- Activity panel with limited recent history
- Status bar feedback
- Threaded action execution to keep the UI responsive
- Loguru-based logging
- Command execution layer for blocking tasks and fire-and-forget app launches
- Local folder opener
- Git repository selector from a configured workspace directory
- Git actions for the selected repository
- Monitoring actions for selected services and processes

## Project Structure

```text
.
├── actions/
│   ├── app_actions.py
│   ├── git_actions.py
│   ├── monitoring_actions.py
│   ├── path_actions.py
│   ├── registry.py
│   ├── system_actions.py
│   └── work_actions.py
├── config/
│   └── commands.py
├── controllers/
│   └── action_controller.py
├── core/
│   ├── command_executor.py
│   ├── logging_setup.py
│   └── repo_scanner.py
├── state/
│   └── app_state.py
├── ui/
│   ├── layout.py
│   └── theme.py
├── main.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Requirements

- Python 3.11+
- Windows OS recommended for the current command set
- ttkbootstrap
- loguru

Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
ttkbootstrap
loguru
```

## Configuration

Local commands are configured in:

```text
config/commands.py
```

Example:

```python
WORKSPACE_DIR = r"C:\Users\user\workspace\development\AI_Projects_2025"

COMMANDS = {
    "vscode": "code",
    "terminal": "start powershell",
    "project_folder": r'explorer "C:\Users\user\workspace\development\AI_Projects_2025"',
    "vs_insiders": r'"C:\Program Files\Microsoft Visual Studio\18\Insiders\Common7\IDE\devenv.exe"',
    "ssms_22": r'"C:\Program Files\Microsoft SQL Server Management Studio 22\Release\Common7\IDE\SSMS.exe"',
    "jira_tickets_url": "https://your-jira-url",
    "chat_gpt_codex": "https://chatgpt.com/codex/cloud",
}
```

Update paths and URLs according to your local machine before running.

## Running the App

```bash
python main.py
```

## Architecture Notes

The application follows a layered structure:

- `ui/`: Tkinter and ttkbootstrap layout/styling only
- `controllers/`: button execution flow, threading, UI feedback, activity updates
- `actions/`: user-facing operations
- `core/`: reusable infrastructure such as command execution, logging, and repo scanning
- `config/`: local command/path configuration
- `state/`: lightweight runtime state such as selected Git repository

Long-running or blocking commands should not run directly inside Tkinter callbacks. Use the controller layer and background thread pattern already implemented in the project.

## Roadmap

- Add confirmation prompts for risky actions such as `git pull`
- Add output/details panel for long command results
- Add configurable actions from JSON or YAML
- Add process/service health cards
- Add search/filter bar for actions
- Add settings screen for workspace and command paths
- Add packaging with PyInstaller

## License

This project is licensed under the MIT License.
