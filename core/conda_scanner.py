from config.commands import COMMANDS
from core.command_executor import run_command


def list_conda_env_names():
    output = run_command(COMMANDS["conda_envs"], timeout=30)

    env_names = []

    for line in output.splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split()

        if not parts:
            continue

        env_name = parts[0]

        if env_name == "*":
            continue

        env_names.append(env_name)

    return env_names