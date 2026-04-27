import sys
from pathlib import Path
from config.commands import COMMANDS
from core.command_executor import  run_command


def list_conda_envs():
    output = run_command(COMMANDS["conda_envs"], timeout=30)

    env_names = []

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        parts = line.split()

        if not parts:
            continue

        env_name = parts[0]

        if env_name == "*":
            continue

        env_names.append(env_name)

    if not env_names:
        return "No Conda environments found"

    return "Conda environments:\n" + "\n".join(f"- {env}" for env in env_names)


def export_current_env():
    env_dir = Path(sys.prefix)
    output_file = Path.cwd() / "environment.yml"

    output = run_command(COMMANDS["conda_export_env"], timeout=120)

    output_file.write_text(output, encoding="utf-8")

    return f"Exported current Conda env to: {output_file.name}"