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
            dpg.add_theme_color(dpg.mvThemeCol_Text, (25, 25, 25))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (170, 170, 170))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (240, 240, 240))

        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (220, 220, 220))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (200, 200, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (180, 180, 180))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (20, 20, 20))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (150, 150, 150))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)

        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_Border, (150, 150, 150))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (25, 25, 25))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)

        with dpg.theme_component(dpg.mvInputInt):
            dpg.add_theme_color(dpg.mvThemeCol_Border, (150, 150, 150))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (230, 230, 230))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (210, 210, 210))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (25, 25, 25))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 5)

        with dpg.theme_component(dpg.mvCombo):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (230, 230, 230))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (210, 210, 210))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)

        with dpg.theme_component(dpg.mvSliderInt):
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (150, 150, 150))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (120, 120, 120))

        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_color(dpg.mvThemeCol_Header, (220, 220, 220))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (200, 200, 200))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (180, 180, 180))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (170, 170, 170))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)

def apply_theme(theme_key):
    theme_tag = THEME_TAGS.get(theme_key, THEME_TAGS[DEFAULT_THEME_KEY])
    dpg.bind_theme(theme_tag)

def get_theme_label_key(theme_key):
    return THEME_LABEL_KEYS.get(theme_key, THEME_LABEL_KEYS[DEFAULT_THEME_KEY])
