from pathlib import Path
import os
import sys


BASE_DIR = Path(__file__).resolve().parents[1]
LOCK_FILE = BASE_DIR / "app.lock"


def acquire_lock():
    if LOCK_FILE.exists():
        try:
            pid = int(LOCK_FILE.read_text())

            # Check if process is still alive
            os.kill(pid, 0)

            # If no exception, process exists
            sys.exit(0)

        except OSError:
            # Stale lock: old process is gone
            LOCK_FILE.unlink()

        except ValueError:
            # Bad lock content
            LOCK_FILE.unlink()

    LOCK_FILE.write_text(str(os.getpid()), encoding="utf-8")


def release_lock():
    if LOCK_FILE.exists():
        try:
            pid = int(LOCK_FILE.read_text())

            # Only remove our own lock
            if pid == os.getpid():
                LOCK_FILE.unlink()

        except Exception:
            pass