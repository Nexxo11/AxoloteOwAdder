import dearpygui.dearpygui as dpg
from src.ow_adder import select_folder, insert_overworld_gui

dpg.create_context()

with dpg.window(tag="primary_window", label="Insert Overworld", width=620, height=460):
    dpg.add_text("Insert Overworld Parameters")
    
    dpg.add_button(label="Select pokeemerald-expansion Folder", callback=select_folder)
    dpg.add_text("If you have a path file config, you don't need to load it again", tag="folder_path_text")
    
    dpg.add_input_text(label="Overworld Name", tag="overworld_name")     
    dpg.add_input_text(label="Overworld ID", tag="overworld_id", default_value="241")
    dpg.add_input_text(label="Palette ID (hex)", tag="palette_id", default_value="1125")
    
    dpg.add_combo(label="Width", items=["16", "32", "64"], tag="width", default_value="32")
    dpg.add_combo(label="Height", items=["16", "32", "64"], tag="height", default_value="32")

    dpg.add_input_int(label="Frame Number", tag="frame_num", default_value=9)
    dpg.add_input_text(label="Reflection Palette Tag", tag="reflection_palette_tag", default_value="OBJ_EVENT_PAL_TAG_NONE")
    dpg.add_combo(label="Palette Slot", items=["PALSLOT_PLAYER", "PALSLOT_NPC_1", "PALSLOT_NPC_2", "PALSLOT_NPC_3", "PALSLOT_NPC_4", "PALSLOT_NPC_5", "PALSLOT_NPC_6", "PALSLOT_NPC_7"], tag="palette_slot", default_value="PALSLOT_NPC_1")
    dpg.add_combo(label="Shadow Size", items=["SHADOW_SIZE_S", "SHADOW_SIZE_M", "SHADOW_SIZE_L", "SHADOW_SIZE_XL"], tag="shadow_size", default_value="SHADOW_SIZE_M")
    dpg.add_combo(label="Inanimate", items=["TRUE", "FALSE"], tag="inanimate", default_value="FALSE")
    dpg.add_combo(label="Tracks", items=["TRUE", "FALSE"], tag="tracks", default_value="FALSE")

    dpg.add_button(label="Insert Overworld", callback=insert_overworld_gui)
    dpg.add_text("", tag="status_text")

    dpg.add_text("By Nexxo", pos=(500, 25))
    dpg.add_text("Compatible expansion version: 1.9.0")


with dpg.window(tag="test", label="Test", width=620, height=460, pos=(630, 0)):

    dpg.add_text("Compatible expansion version: 1.9.0")


dpg.create_viewport(title='AxoloteOwAdder', width=1280, height=720, resizable=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
