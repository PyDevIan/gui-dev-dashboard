from datetime import datetime
import threading

import ttkbootstrap as ttk
from loguru import logger


def run_action(action, status_label, button, activity_list):
    update_button_state(button, "disabled")

    thread = threading.Thread(
        target=_execute_action,
        args=(action, status_label, button, activity_list),
        daemon=True,
    )
    thread.start()


def _execute_action(action, status_label, button, activity_list):
    label = action["label"]
    handler = action["handler"]
    action_type = action.get("type", "task")

    try:
        if action_type == "launch":
            update_status(status_label, f"Launching: {label}")
            logger.info(f"Launching action: {label}")

            handler()

            update_status(status_label, f"Launched: {label}")
            add_activity(activity_list, f"Launched {label}")
            logger.info(f"Launched action: {label}")

        else:
            update_status(status_label, f"Running: {label}")
            logger.info(f"Started action: {label}")

            result_message = handler()
            message = result_message or f"Completed: {label}"

            update_status(status_label, message)
            add_activity(activity_list, message)
            logger.info(message)

    except Exception:
        update_status(status_label, f"Failed: {label}")
        add_activity(activity_list, f"Failed {label}")
        logger.exception(f"Failed action: {label}")

    finally:
        update_button_state(button, "normal")


def update_status(status_label, message):
    status_label.after(
        0,
        lambda: status_label.config(text=message),
    )


def update_button_state(button, state):
    button.after(
        0,
        lambda: button.configure(state=state),
    )


MAX_ACTIVITY_ITEMS = 12


def add_activity(activity_list, message):
    timestamp = datetime.now().strftime("%H:%M:%S")

    def _add():
        for widget in activity_list.winfo_children():
            try:
                if widget.cget("text") == "No recent activity":
                    widget.destroy()
            except Exception:
                pass

        item = ttk.Label(
            activity_list,
            text=f"{timestamp}  {message}",
            style="Description.TLabel",
            wraplength=220,
        )
        item.pack(anchor="w", pady=(0, 8))

        children = activity_list.winfo_children()

        if len(children) > MAX_ACTIVITY_ITEMS:
            children[0].destroy()

    activity_list.after(0, _add)