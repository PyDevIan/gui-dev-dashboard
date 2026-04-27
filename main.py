import os
from pathlib import Path

import ttkbootstrap as ttk

from actions.registry import ACTIONS
from core.logging_setup import setup_logging
from core.single_instance import acquire_lock, release_lock
from ui.layout import build_main_layout
from ui.theme import APP_THEME, apply_custom_styles

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

acquire_lock()
try:
    logger = setup_logging(
        log_file=Path("logs/control_panel.log"),
        level="INFO",
    )

    app = ttk.Window(themename=APP_THEME)
    apply_custom_styles(app.style)
    app.title("Developer Control Panel")
    app.geometry("1420x960")

    build_main_layout(app, ACTIONS)

    app.mainloop()

except Exception:
    import traceback

    with open("startup_error.log", "w", encoding="utf-8") as f:
        f.write(traceback.format_exc())

finally:
    release_lock()
