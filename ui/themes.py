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

def setup_themes():
    with dpg.theme(tag=THEME_TAGS["purple"]):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 230, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (100, 70, 120))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (30, 30, 30))

        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (80, 80, 80))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (100, 100, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (120, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (120, 120, 180))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)

        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_Border, (80, 60, 120))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 230, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)

        with dpg.theme_component(dpg.mvInputInt):
            dpg.add_theme_color(dpg.mvThemeCol_Border, (80, 60, 120))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (70, 70, 100))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (90, 90, 130))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 230, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 5)

        with dpg.theme_component(dpg.mvCombo):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 50, 100))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (80, 80, 200))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)

        with dpg.theme_component(dpg.mvSliderInt):
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (120, 80, 180))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (150, 100, 200))

        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 60, 80))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (80, 80, 120))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (100, 100, 150))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (50, 50, 80))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)

    with dpg.theme(tag=THEME_TAGS["light"]):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (245, 252, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (245, 252, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (20, 35, 40)) # Darker text for better contrast
            dpg.add_theme_color(dpg.mvThemeCol_Border, (180, 210, 220))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255)) # Pure white inputs
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (225, 245, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (200, 235, 250))
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 6)

        # --- Interactive Elements (Buttons) ---
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 160, 190))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 190, 220))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 140, 170))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 6)

        # --- Inputs & Others ---
        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 160, 190))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255))

        with dpg.theme_component(dpg.mvInputInt):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 160, 190))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 190, 220))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 140, 170))

        with dpg.theme_component(dpg.mvCombo):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 160, 190))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 190, 220))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (200, 240, 255))

        with dpg.theme_component(dpg.mvSliderInt):
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (0, 160, 190))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (0, 130, 160))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (200, 220, 230))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (180, 210, 225))

        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 160, 190))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (0, 190, 220))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 130, 160))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 8)

        with dpg.theme_component(dpg.mvSeparator):
            dpg.add_theme_color(dpg.mvThemeCol_Separator, (0, 160, 190, 100))


def apply_theme(theme_key):
    theme_tag = THEME_TAGS.get(theme_key, THEME_TAGS[DEFAULT_THEME_KEY])
    dpg.bind_theme(theme_tag)

def get_theme_label_key(theme_key):
    return THEME_LABEL_KEYS.get(theme_key, THEME_LABEL_KEYS[DEFAULT_THEME_KEY])
