import subprocess

from loguru import logger


def run_command(command, timeout=30, cwd=None):
    logger.debug(f"Running command: {command} | cwd={cwd}")

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=cwd,
    )

    if result.returncode != 0:
        error_message = result.stderr.strip() or "Unknown command error"
        raise RuntimeError(error_message)

    return result.stdout.strip()


def launch_command(command):
    logger.debug(f"Launching command: {command}")

    subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )