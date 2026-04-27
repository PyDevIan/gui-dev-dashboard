import threading
from pathlib import Path

import pystray
from PIL import Image

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
