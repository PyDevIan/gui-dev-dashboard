from collections import defaultdict

import ttkbootstrap as ttk
from controller.action_controler import add_activity
from ttkbootstrap.constants import *

from actions.path_actions import open_folder_path
from controller.action_controler import run_action
from state import app_state
from core.repo_scanner import find_git_repositories
from tkinter import messagebox

def build_main_layout(app, actions):
    main_frame = ttk.Frame(app, padding=0, style="Main.TFrame")
    main_frame.pack(fill=BOTH, expand=True)

    status_label = create_status_bar(app)

    sidebar = create_sidebar_shell(main_frame)

    content = create_content_area(main_frame)
    dashboard_panel = create_dashboard_panel(content)

    add_header(dashboard_panel)
    add_stats_row(dashboard_panel, actions)

    actions_panel, activity_panel = create_dashboard_body(dashboard_panel)

    activity_list = add_activity_panel(activity_panel)
    add_section_header(
        actions_panel,
        "Quick Actions",
        "Launch tools, scripts, and workflows from here.",
    )
    add_git_repo_selector(actions_panel, status_label, activity_list)
    add_path_opener(actions_panel, status_label, activity_list)

    action_area = create_scrollable_area(actions_panel)

    populate_sidebar(
        sidebar,
        actions,
        action_area,
        status_label,
        activity_list,
    )

    render_actions(action_area, actions, status_label, activity_list)


def create_sidebar_shell(parent):
    sidebar = ttk.Frame(parent, width=180, padding=14, style="Panel.TFrame")
    sidebar.pack(side=LEFT, fill=Y)
    sidebar.pack_propagate(False)

    logo = ttk.Label(
        sidebar,
        text="DEV PANEL",
        style="SidebarTitle.TLabel",
    )
    logo.pack(anchor="w", pady=(0, 25))

    return sidebar


def populate_sidebar(sidebar, actions, action_area, status_label, activity_list):
    categories = sorted({action["category"] for action in actions})
    nav_items = ["Dashboard"] + categories
    nav_buttons = {}

    for item in nav_items:
        button = ttk.Button(
            sidebar,
            text=item,
            style="Sidebar.TButton",
            bootstyle="info-outline",
        )

        button.configure(
            command=lambda selected=item: handle_sidebar_click(
                selected,
                actions,
                action_area,
                status_label,
                activity_list,
                nav_buttons,
            )
        )

        button.pack(fill=X, pady=6)
        nav_buttons[item] = button

    set_active_sidebar_button(nav_buttons, "Dashboard")

def set_active_sidebar_button(nav_buttons, selected):
    for name, button in nav_buttons.items():
        if name == selected:
            button.configure(bootstyle="info")
        else:
            button.configure(bootstyle="info-outline")

def handle_sidebar_click(
    selected,
    actions,
    action_area,
    status_label,
    activity_list,
    nav_buttons,
):
    if selected == "Dashboard":
        filtered_actions = actions
    else:
        filtered_actions = [
            action for action in actions
            if action["category"] == selected
        ]

    render_actions(action_area, filtered_actions, status_label, activity_list)
    status_label.config(text=f"Viewing: {selected}")
    set_active_sidebar_button(nav_buttons, selected)


def create_content_area(parent):
    content = ttk.Frame(parent, padding=30, style="Main.TFrame")
    content.pack(side=LEFT, fill=BOTH, expand=True)
    return content


def create_dashboard_panel(parent):
    panel = ttk.Frame(parent, padding=24, style="Panel.TFrame")
    panel.pack(fill=BOTH, expand=True)
    return panel


def add_header(parent):
    title = ttk.Label(
        parent,
        text="Developer Control Panel",
        style="Title.TLabel",
    )
    title.pack(anchor="w", pady=(0, 8))

    subtitle = ttk.Label(
        parent,
        text="Select an action to begin",
        style="Subtitle.TLabel",
    )
    subtitle.pack(anchor="w", pady=(0, 20))


def add_stats_row(parent, actions):
    stats_frame = ttk.Frame(parent, style="Panel.TFrame")
    stats_frame.pack(fill=X, pady=(0, 10))
    
    categories = {action["category"] for action in actions}

    stats = [
        ("Actions", len(actions)),
        ("Categories", len(categories)),
        ("Status", "Ready"),
    ]

    for label, value in stats:
        card = ttk.Frame(stats_frame, padding=14, style="Card.TFrame")
        card.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))

        value_label = ttk.Label(
            card,
            text=str(value),
            style="Title.TLabel",
        )
        value_label.pack(anchor="w")

        name_label = ttk.Label(
            card,
            text=label,
            style="Description.TLabel",
        )
        name_label.pack(anchor="w")


def create_dashboard_body(parent):
    body = ttk.Frame(parent, style="Panel.TFrame")
    body.pack(fill=BOTH, expand=True)

    actions_panel = ttk.Frame(body, style="Panel.TFrame")
    actions_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 16))

    activity_panel = ttk.Frame(body, width=260, padding=16, style="Card.TFrame")
    activity_panel.pack(side=RIGHT, fill=Y)
    activity_panel.pack_propagate(False)

    return actions_panel, activity_panel


def add_section_header(parent, title, subtitle):
    frame = ttk.Frame(parent, style="Panel.TFrame")
    frame.pack(fill=X, pady=(0, 10))

    title_label = ttk.Label(
        frame,
        text=title,
        style="Section.TLabel",
    )
    title_label.pack(anchor="w")

    subtitle_label = ttk.Label(
        frame,
        text=subtitle,
        style="Subtitle.TLabel",
    )
    subtitle_label.pack(anchor="w")


def create_scrollable_area(parent):
    container = ttk.Frame(parent, style="Panel.TFrame")
    container.pack(fill=BOTH, expand=True)

    canvas = ttk.Canvas(
        container,
        height=360,
        highlightthickness=0,
        background="#0B1A2A",
    )

    scrollbar = ttk.Scrollbar(
        container,
        orient=VERTICAL,
        command=canvas.yview,
        bootstyle="round",
    )

    scrollable_frame = ttk.Frame(canvas, style="Panel.TFrame")

    canvas_window = canvas.create_window(
        (0, 0),
        window=scrollable_frame,
        anchor="nw",
    )

    scrollable_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
    )

    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(canvas_window, width=event.width),
    )

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    return scrollable_frame


def add_action_sections(parent, actions, status_label, activity_list):
    grouped_actions = defaultdict(list)

    for action in actions:
        grouped_actions[action["category"]].append(action)

    for category, category_actions in grouped_actions.items():
        category_label = ttk.Label(
            parent,
            text=category,
            style="Section.TLabel",
        )
        category_label.pack(anchor="w", pady=(10, 8))

        for action in category_actions:
            create_action_card(parent, action, status_label, activity_list)


def create_action_card(parent, action, status_label, activity_list):
    card = ttk.Frame(parent, padding=12, style="Card.TFrame")
    card.pack(fill=X, pady=6, padx=(0, 8))

    button = ttk.Button(
        card,
        text=action["label"],
        bootstyle=action["style"],
        width=20,
    )

    def handle_button_click():
        if action.get("confirm"):
            confirmed = messagebox.askyesno(
                "Confirm Action",
                action.get("confirm_message", f"Run {action['label']}?"),
            )

            if not confirmed:
                return

        run_action(action, status_label, button, activity_list)

    button.configure(command=handle_button_click)

    button.pack(side=LEFT, padx=(0, 16))

    description = ttk.Label(
        card,
        text=action.get("description", ""),
        style="Description.TLabel",
        anchor="w",
    )
    description.pack(side=LEFT, fill=X, expand=True)


def create_status_bar(parent):
    status = ttk.Label(
        parent,
        text="Ready",
        padding=8,
        anchor="w",
        style="Status.TLabel",
    )
    status.pack(side=BOTTOM, fill=X)

    return status


def add_activity_panel(parent):
    title = ttk.Label(
        parent,
        text="Activity",
        style="Section.TLabel",
    )
    title.pack(anchor="w", pady=(0, 10))

    activity_list = ttk.Frame(parent, style="Card.TFrame")
    activity_list.pack(fill=BOTH, expand=True)

    empty = ttk.Label(
        activity_list,
        text="No recent activity",
        style="Description.TLabel",
        wraplength=220,
    )
    empty.pack(anchor="w")

    return activity_list


def render_actions(parent, actions, status_label, activity_list):
    for widget in parent.winfo_children():
        widget.destroy()

    add_action_sections(parent, actions, status_label, activity_list)


def add_path_opener(parent, status_label, activity_list):
    wrapper = ttk.Frame(parent, padding=12, style="Card.TFrame")
    wrapper.pack(fill=X, pady=(0, 16))

    title = ttk.Label(
        wrapper,
        text="Open Local Folder",
        style="Section.TLabel",
    )
    title.pack(anchor="w", pady=(0, 8))

    row = ttk.Frame(wrapper, style="Card.TFrame")
    row.pack(fill=X)

    path_entry = ttk.Entry(row)
    path_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))

    def handle_open_path():
        try:
            result = open_folder_path(path_entry.get())
            status_label.config(text=result)
            add_activity(activity_list, result)
        except Exception as error:
            message = f"Failed to open folder: {error}"
            status_label.config(text=message)
            add_activity(activity_list, message)

    open_button = ttk.Button(
        row,
        text="Open",
        bootstyle="info",
        command=handle_open_path,
    )
    open_button.pack(side=RIGHT)

def add_git_repo_selector(parent, status_label, activity_list):
    repos = find_git_repositories()
    repo_names = [repo.name for repo in repos]
    repo_map = {repo.name: repo for repo in repos}

    wrapper = ttk.Frame(parent, padding=12, style="Card.TFrame")
    wrapper.pack(fill=X, pady=(0, 16))

    title = ttk.Label(
        wrapper,
        text="Selected Git Repository",
        style="Section.TLabel",
    )
    title.pack(anchor="w", pady=(0, 8))

    row = ttk.Frame(wrapper, style="Card.TFrame")
    row.pack(fill=X)

    repo_combo = ttk.Combobox(
        row,
        values=repo_names,
        state="readonly",
    )
    repo_combo.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
    if repo_names:
        repo_combo.current(0)

    def handle_set_repo():
        selected_name = repo_combo.get()

        if not selected_name:
            message = "No repository selected"
            status_label.config(text=message)
            add_activity(activity_list, message)
            return

        selected_path = repo_map[selected_name]
        app_state.selected_repo_path = str(selected_path)

        message = f"Selected repo: {selected_name}"
        status_label.config(text=message)
        add_activity(activity_list, message)

    set_button = ttk.Button(
        row,
        text="Set Repo",
        bootstyle="success",
        command=handle_set_repo,
    )
    set_button.pack(side=RIGHT)