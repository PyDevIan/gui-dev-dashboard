APP_THEME = "darkly"

COLORS = {
    "app_bg": "#07111F",
    "panel_bg": "#0B1A2A",
    "card_bg": "#102235",
    "text": "#EAF2FF",
    "muted": "#8FA8C6",
    "blue": "#1E90FF",
    "green": "#22C55E",
    "purple": "#8B5CF6",
}

FONTS = {
    "title": ("Segoe UI", 22, "bold"),
    "subtitle": ("Segoe UI", 11),
    "section": ("Segoe UI", 13, "bold"),
    "button": ("Segoe UI", 10, "bold"),
    "description": ("Segoe UI", 10),
    "sidebar_title": ("Segoe UI", 16, "bold"),
    "sidebar": ("Segoe UI", 10),
}


def apply_custom_styles(style):
    style.configure(
        "Main.TFrame",
        background=COLORS["app_bg"],
    )

    style.configure(
        "Panel.TFrame",
        background=COLORS["panel_bg"],
    )

    style.configure(
        "Card.TFrame",
        background=COLORS["card_bg"],
    )

    style.configure(
        "Title.TLabel",
        background=COLORS["panel_bg"],
        foreground=COLORS["text"],
        font=FONTS["title"],
    )

    style.configure(
        "Subtitle.TLabel",
        background=COLORS["panel_bg"],
        foreground=COLORS["muted"],
        font=FONTS["subtitle"],
    )

    style.configure(
        "Section.TLabel",
        background=COLORS["panel_bg"],
        foreground=COLORS["blue"],
        font=FONTS["section"],
    )

    style.configure(
        "Description.TLabel",
        background=COLORS["card_bg"],
        foreground=COLORS["muted"],
        font=FONTS["description"],
    )

    style.configure(
        "Status.TLabel",
        background=COLORS["panel_bg"],
        foreground=COLORS["muted"],
        font=FONTS["subtitle"],
    )

    style.configure(
        "Sidebar.TLabel",
        background=COLORS["panel_bg"],
        foreground=COLORS["muted"],
        font=FONTS["subtitle"],
        padding=8,
    )

    style.configure(
        "SidebarTitle.TLabel",
        background=COLORS["panel_bg"],
        foreground=COLORS["text"],
        font=FONTS["sidebar_title"],
    )

    style.configure(
        "Sidebar.TButton",
        font=FONTS["sidebar"],
        padding=(10, 8),
    )
    style.configure(
        "SidebarActive.TButton",
        font=FONTS["sidebar"],
        padding=(10, 8),
    )       