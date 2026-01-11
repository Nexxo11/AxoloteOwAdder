import dearpygui.dearpygui as dpg

DEFAULT_THEME_KEY = "purple"

THEME_TAGS = {
    "purple": "purple_theme",
    "light": "light_theme",
}

THEME_LABEL_KEYS = {
    "purple": "theme_purple",
    "light": "theme_light",
}

# Extra themes for per-item binding (primary / danger buttons)
PRIMARY_BUTTON_THEME_TAGS = {
    "purple": "purple_primary_button",
    "light": "light_primary_button",
}
DANGER_BUTTON_THEME_TAGS = {
    "purple": "purple_danger_button",
    "light": "light_danger_button",
}


def setup_themes():
    # =========================
    # PURPLE (Dark) - Base Theme
    # =========================
    PURPLE_ACCENT = (140, 110, 220)
    PURPLE_ACCENT_HOVER = (160, 130, 240)
    PURPLE_ACCENT_ACTIVE = (120, 95, 200)

    P_TEXT = (235, 235, 255)
    P_TEXT_MUTED = (170, 170, 195)

    P_BG = (22, 22, 26)
    P_PANEL = (30, 30, 36)
    P_PANEL_ALT = (38, 38, 46)

    P_BORDER = (90, 70, 120)
    P_BORDER_SOFT = (70, 55, 95)

    with dpg.theme(tag=THEME_TAGS["purple"]):
        with dpg.theme_component(dpg.mvAll):
            # Backgrounds
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, P_BG)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, P_BG)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, P_PANEL)

            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (26, 26, 32))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (26, 26, 32))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (26, 26, 32))

            # Text
            dpg.add_theme_color(dpg.mvThemeCol_Text, P_TEXT)
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, P_TEXT_MUTED)

            # Borders & separators
            dpg.add_theme_color(dpg.mvThemeCol_Border, P_BORDER_SOFT)
            dpg.add_theme_color(dpg.mvThemeCol_Separator, (90, 70, 120, 160))

            # Frames (inputs, combo, etc.)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, P_PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, P_PANEL_ALT)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (46, 46, 58))

            # Scrollbar
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (24, 24, 30))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (70, 60, 95))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (90, 75, 125))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (110, 90, 155))

            # Rounding / spacing
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 8)

            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 8)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 4)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 14, 12)

        # Buttons (default: neutral)
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (55, 55, 65))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (68, 68, 82))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (80, 80, 100))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, P_BORDER)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 14, 8)

        # Inputs
        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, P_PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_Border, P_BORDER_SOFT)
            dpg.add_theme_color(dpg.mvThemeCol_Text, P_TEXT)

        with dpg.theme_component(dpg.mvInputInt):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, P_PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_Border, P_BORDER_SOFT)
            dpg.add_theme_color(dpg.mvThemeCol_Text, P_TEXT)

        # Combo
        with dpg.theme_component(dpg.mvCombo):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, P_PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_Border, P_BORDER_SOFT)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, P_PANEL_ALT)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (46, 46, 58))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)

        # Slider
        with dpg.theme_component(dpg.mvSliderInt):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 50))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 50, 65))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, PURPLE_ACCENT)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, PURPLE_ACCENT_ACTIVE)

        # Collapsing Header (neutral, not accent)
        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_color(dpg.mvThemeCol_Header, (40, 40, 50))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (52, 52, 66))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (62, 62, 78))
            dpg.add_theme_color(dpg.mvThemeCol_Text, P_TEXT)
            dpg.add_theme_color(dpg.mvThemeCol_Border, P_BORDER_SOFT)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 10)

        with dpg.theme_component(dpg.mvSeparator):
            dpg.add_theme_color(dpg.mvThemeCol_Separator, (90, 70, 120, 160))

    # PURPLE - Primary Button Theme
    with dpg.theme(tag=PRIMARY_BUTTON_THEME_TAGS["purple"]):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, PURPLE_ACCENT)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, PURPLE_ACCENT_HOVER)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, PURPLE_ACCENT_ACTIVE)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0))
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 16, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)

    # PURPLE - Danger Button Theme
    with dpg.theme(tag=DANGER_BUTTON_THEME_TAGS["purple"]):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 55, 75))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (220, 70, 90))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (175, 40, 60))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0))
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 16, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)

    # =========================
    # LIGHT (Professional) - Base Theme
    # =========================
    ACCENT = (0, 140, 170)
    ACCENT_HOVER = (0, 155, 190)
    ACCENT_ACTIVE = (0, 120, 145)

    TEXT = (18, 22, 28)
    BG = (246, 248, 252)
    PANEL = (255, 255, 255)
    PANEL_ALT = (242, 245, 250)
    BORDER = (210, 218, 230)

    with dpg.theme(tag=THEME_TAGS["light"]):
        with dpg.theme_component(dpg.mvAll):
            # Backgrounds
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, BG)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, BG)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (235, 238, 244))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (235, 238, 244))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (235, 238, 244))

            # Text
            dpg.add_theme_color(dpg.mvThemeCol_Text, TEXT)
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (150, 160, 175))

            # Borders & separators
            dpg.add_theme_color(dpg.mvThemeCol_Border, BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_Separator, (210, 218, 230, 180))

            # Frames
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (248, 250, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (240, 246, 255))

            # Scrollbar
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (240, 243, 248))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (200, 210, 225))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (185, 198, 218))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (170, 186, 210))

            # Rounding / spacing
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 8)

            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 8)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 4)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 14, 12)

        # Buttons (default neutral)
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, PANEL_ALT)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (235, 240, 248))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (225, 233, 245))
            dpg.add_theme_color(dpg.mvThemeCol_Border, BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_Text, TEXT)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 14, 8)

        # Inputs
        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_Border, BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))

        with dpg.theme_component(dpg.mvInputInt):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_Border, BORDER)

        # Combo
        with dpg.theme_component(dpg.mvCombo):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_Border, BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (230, 240, 248))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (220, 234, 246))

        # Slider
        with dpg.theme_component(dpg.mvSliderInt):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (230, 236, 245))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (220, 229, 242))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, ACCENT)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, ACCENT_ACTIVE)

        # Collapsing Header (neutral)
        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_color(dpg.mvThemeCol_Header, (235, 240, 248))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (225, 233, 245))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (215, 226, 242))
            dpg.add_theme_color(dpg.mvThemeCol_Text, TEXT)
            dpg.add_theme_color(dpg.mvThemeCol_Border, BORDER)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 10)

        with dpg.theme_component(dpg.mvSeparator):
            dpg.add_theme_color(dpg.mvThemeCol_Separator, (210, 218, 230, 180))

    # LIGHT - Primary Button Theme
    with dpg.theme(tag=PRIMARY_BUTTON_THEME_TAGS["light"]):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, ACCENT)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, ACCENT_HOVER)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, ACCENT_ACTIVE)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0))
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 16, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)

    # LIGHT - Danger Button Theme
    with dpg.theme(tag=DANGER_BUTTON_THEME_TAGS["light"]):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (220, 60, 80))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (235, 75, 95))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (195, 45, 65))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0))
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 16, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)


def apply_theme(theme_key: str):
    theme_tag = THEME_TAGS.get(theme_key, THEME_TAGS[DEFAULT_THEME_KEY])
    dpg.bind_theme(theme_tag)


def get_theme_label_key(theme_key: str) -> str:
    return THEME_LABEL_KEYS.get(theme_key, THEME_LABEL_KEYS[DEFAULT_THEME_KEY])


def get_primary_button_theme_tag(theme_key: str) -> str:
    """Bind this theme to the main CTA button (Insert Overworld)."""
    return PRIMARY_BUTTON_THEME_TAGS.get(theme_key, PRIMARY_BUTTON_THEME_TAGS[DEFAULT_THEME_KEY])


def get_danger_button_theme_tag(theme_key: str) -> str:
    """Bind this theme to destructive actions (Delete)."""
    return DANGER_BUTTON_THEME_TAGS.get(theme_key, DANGER_BUTTON_THEME_TAGS[DEFAULT_THEME_KEY])
