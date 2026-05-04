import ctypes
import os
import threading
from pathlib import Path

import pystray
from PIL import Image

APP_ID = "giannis.dev.controlpanel"


BASE_DIR = Path(__file__).resolve().parents[1]
ICON_PATH = BASE_DIR / "icon.ico"


def create_tray_icon(app):
    image = Image.open(ICON_PATH)

    menu = pystray.Menu(
        pystray.MenuItem("Show", lambda: show_window(app)),
        pystray.MenuItem("Exit", lambda icon: exit_app(icon, app)),
    )

    icon = pystray.Icon(
        "dev_control_panel",
        image,
        "Dev Control Panel",
        menu,
    )

    thread = threading.Thread(target=icon.run, daemon=True)
    thread.start()

    return icon


def hide_to_tray(app):
    app.withdraw()


def show_window(app):
    app.after(0, app.deiconify)
    app.after(0, app.lift)


def exit_app(icon, app):
    icon.stop()
    app.after(0, app.destroy)


def set_windows_window_icon(window, icon_path: Path, logger=None):
    """Set icon for title bar and taskbar reliably on Windows."""
    icon_str = str(icon_path)

    # Tk title bar icon.
    window.iconbitmap(icon_str)

    if os.name != "nt":
        return

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

    image_icon = 1
    lr_loadfromfile = 0x0010
    lr_defaultsize = 0x0040
    wm_seticon = 0x0080
    icon_small = 0
    icon_big = 1

    # Use window handle directly; GetParent can point at the wrong HWND.
    hwnd = int(window.winfo_id())
    parent_hwnd = ctypes.windll.user32.GetParent(hwnd)

    hicon = ctypes.windll.user32.LoadImageW(
        0,
        icon_str,
        image_icon,
        0,
        0,
        lr_loadfromfile | lr_defaultsize,
    )

    if not hicon:
        if logger:
            logger.warning("Could not load icon resource for taskbar: {}", icon_str)
        return

    targets = [hwnd]
    if parent_hwnd and parent_hwnd != hwnd:
        targets.append(parent_hwnd)

    for target in targets:
        ctypes.windll.user32.SendMessageW(target, wm_seticon, icon_small, hicon)
        ctypes.windll.user32.SendMessageW(target, wm_seticon, icon_big, hicon)

    if logger:
        logger.debug(
            "Applied window icon. hwnd={}, parent_hwnd={}, hicon={}",
            hwnd,
            parent_hwnd,
            hicon,
        )


def apply_icon_with_retry(window, icon_path: Path, logger=None):
    """Re-apply icon after the window is realized to fix first-launch taskbar fallback."""
    set_windows_window_icon(window, icon_path, logger=logger)
    window.after(250, lambda: set_windows_window_icon(window, icon_path, logger=logger))
