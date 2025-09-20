import dearpygui.dearpygui as dpg
from core.config import complete_config

def setup_popups(translator):
    with dpg.window(tag="popup_window", label="Configure Project", modal=True, show=False, no_resize=True, no_close=True):
        dpg.add_text("Select the option that matches your project")
        dpg.add_combo(items=["Pokeemerald", "Poke-expansion"], tag="project_setting_ver", default_value="Poke-expansion")
        dpg.add_separator()
        dpg.add_checkbox(label="Dynamic Pal System", tag="project_setting_pal", default_value=True)
        dpg.add_separator()
        dpg.add_button(label="Complete", callback=lambda: complete_config(translator))
