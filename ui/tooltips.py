import dearpygui.dearpygui as dpg

def setup_tooltips():
    with dpg.tooltip("menu_language"):
        dpg.add_text("Click to change the UI language.", tag="translate_tooltip_text")
    with dpg.tooltip("verify_version"):
        dpg.add_text("Click to check for the latest version.")
    with dpg.tooltip("select_folder_button"):
        dpg.add_text("Click to select the project folder")
    with dpg.tooltip("select_ow_button"):
        dpg.add_text("Click to select the new overworld to add to your project")
    with dpg.tooltip("overworld_name"):
        dpg.add_text("Enter the name of the overworld character.\nExample: GARY.")
    with dpg.tooltip("width"):
        dpg.add_text("Select the width of the overworld sprite.")
    with dpg.tooltip("height"):
        dpg.add_text("Select the height of the overworld sprite.")
    with dpg.tooltip("frame_num"):
        dpg.add_text("Enter the number of frames for the overworld animation.")
    with dpg.tooltip("reflection_palette_tag"):
        dpg.add_text("Enter the reflection palette tag, or leave as default.")
    with dpg.tooltip("palette_slot"):
        dpg.add_text("Select the palette slot for the overworld.")
    with dpg.tooltip("anim_table"):
        dpg.add_text("Select the Anim Table for the overworld.")
    with dpg.tooltip("shadow_size"):
        dpg.add_text("Select the size of the shadow beneath the overworld.")
    with dpg.tooltip("inanimate"):
        dpg.add_text("Set to TRUE if the overworld should not animate.")
    with dpg.tooltip("tracks"):
        dpg.add_text("Set to TRUE if the overworld should leave tracks when moving.")
    with dpg.tooltip("pal_tag_txt"):
        dpg.add_text("if not using Dynamic Pal System.")
    with dpg.tooltip("pal_tag"):
        dpg.add_text("if not using Dynamic Pal System.")
    with dpg.tooltip("insert_button"):
        dpg.add_text("Click to insert the overworld into the game.")
    with dpg.tooltip("refresh_list_btn"):
        dpg.add_text("Refresh the list of installed overworlds.", tag="refresh_tooltip_text")
