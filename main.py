import os
from pathlib import Path

import ttkbootstrap as ttk

from actions.registry import ACTIONS
from core.logging_setup import setup_logging
from core.single_instance import acquire_lock, release_lock
from core.tray import create_tray_icon, hide_to_tray
from ui.layout import build_main_layout
from ui.theme import APP_THEME, apply_custom_styles

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

acquire_lock()

try:
    logger = setup_logging(
        log_file=BASE_DIR / "logs" / "control_panel.log",
        level="INFO",
    )

    app = ttk.Window(themename=APP_THEME)
    apply_custom_styles(app.style)

    app.title("Developer Control Panel")
    app.iconbitmap(BASE_DIR / "icon.ico")
    app.state("zoomed")

    tray_icon = create_tray_icon(app)

    build_main_layout(app, ACTIONS)

    app.protocol("WM_DELETE_WINDOW", lambda: hide_to_tray(app))
    app.mainloop()

except Exception:
    import traceback

    with open(BASE_DIR / "startup_error.log", "w", encoding="utf-8") as f:
        f.write(traceback.format_exc())

finally:
    release_lock()
