import dearpygui.dearpygui as dpg
from src.ow_adder import select_folder, insert_overworld_gui, select_and_move_sprite, verify_version, complete_config
from src.translate import change_language

dpg.create_context()

with dpg.theme(tag="purple_theme"):
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

with dpg.handler_registry():
    dpg.add_key_release_handler(key=dpg.mvKey_Escape, callback=lambda: dpg.stop_dearpygui())

pal_tag_items = [
    "BRENDAN",
    "BRENDAN_REFLECTION",
    "BRIDGE_REFLECTION",
    "NPC_1",
    "NPC_2",
    "NPC_3",
    "NPC_4",
    "NPC_1_REFLECTION",
    "NPC_2_REFLECTION",
    "NPC_3_REFLECTION",
    "NPC_4_REFLECTION",
    "QUINTY_PLUMP",
    "QUINTY_PLUMP_REFLECTION",
    "TRUCK",
    "VIGOROTH",
    "ZIGZAGOON",
    "MAY",
    "MAY_REFLECTION",
    "MOVING_BOX",
    "CABLE_CAR",
    "SSTIDAL",
    "PLAYER_UNDERWATER",
    "KYOGRE",
    "KYOGRE_REFLECTION",
    "GROUDON",
    "GROUDON_REFLECTION",
    "UNUSED",
    "SUBMARINE_SHADOW",
    "POOCHYENA",
    "RED_LEAF",
    "DEOXYS",
    "BIRTH_ISLAND_STONE",
    "HO_OH",
    "LUGIA",
    "RS_BRENDAN",
    "RS_MAY",
    "NONE"
]

with dpg.window(tag="popup_window", label="Configure Project", modal=False, show=False, no_resize=True):
    dpg.add_text("Select the option that matches your project")
    dpg.add_combo(items=["Pokeemerald", "Poke-expansion"], tag="project_setting_ver", default_value="Poke-expansion")
    dpg.add_separator()
    dpg.add_checkbox(label="Dynamic Pal System", tag="project_setting_pal", default_value=True)
    dpg.add_separator()
    dpg.add_button(label="Complete", callback=complete_config)

with dpg.window(tag="primary_window", label="Insert Overworld", width=540, height=580, no_title_bar=True, no_resize=True, no_move=True):

    #dpg.add_combo(items=["en", "es"], default_value="en", callback=change_language, width=100)
    dpg.add_text("", tag="footer_text", pos=(380, 10))

    with dpg.group(horizontal=True):
        dpg.add_button(label="Check for Updates", callback=verify_version, tag="verify_version")
        dpg.add_text("", tag="ver_status_text")
    with dpg.tooltip("verify_version"):
        dpg.add_text("Click to check for the latest version.")
    
    dpg.add_button(label="Select pokeemerald-expansion Folder", callback=select_folder, tag="select_folder_button")
    with dpg.tooltip("select_folder_button"):
        dpg.add_text("Click to select the pokeemerald-expansion folder")

    dpg.add_text("If you have a path file config, you don't need to load it again", tag="folder_path_text", color=(150, 150, 150))
    dpg.add_spacer(height=10)
    dpg.add_separator()
    dpg.add_spacer(height=10)
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=142)
        dpg.add_button(label="Select new overworld to add", callback=select_and_move_sprite, tag="select_ow_button")
    with dpg.tooltip("select_ow_button"):
        dpg.add_text("Click to select the new overworld to add to your project")
    dpg.add_spacer(height=10)
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=100)
        dpg.add_text("Sprite Preview", tag="sprite_txt_preview", color=(150, 150, 150))
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=96)
        with dpg.child_window(tag="sprite_preview", width=300, height=64, border=True):
            dpg.add_text(tag="preview_text")
        with dpg.tooltip("sprite_preview"):
            dpg.add_text("Sprite preview of new overworld")
    dpg.add_spacer(height=10)
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=156)
        dpg.add_text("Overworld Name", tag="overworld_txt_name")
        
        #dpg.add_spacer(width=90)
        #dpg.add_text("Overworld ID")
        #dpg.add_spacer(width=10)
        #dpg.add_text("Palette ID (hex)")
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=146)
        dpg.add_input_text(tag="overworld_name", width=200)
        with dpg.tooltip("overworld_name"):
            dpg.add_text("Enter the name of the overworld character.\nExample: GARY.")

        #dpg.add_input_text(tag="overworld_id", default_value="241", width=100)
        #with dpg.tooltip("overworld_id"):
            #dpg.add_text("Enter the unique ID for the overworld. Default is 241.")

        #dpg.add_input_text(tag="palette_id", default_value="1125", width=100)
        #with dpg.tooltip("palette_id"):
        #    dpg.add_text("Enter the palette ID in hexadecimal format.")

    dpg.add_spacer(height=10)
    dpg.add_separator()
    dpg.add_spacer(height=10)
    
    with dpg.group(horizontal=True):
        dpg.add_text("Width", tag="width_txt")
        dpg.add_combo(items=["16", "32", "64"], tag="width", default_value="32", width=100)
        with dpg.tooltip("width"):
            dpg.add_text("Select the width of the overworld sprite.")
        
        dpg.add_text("Height", tag="height_txt")
        dpg.add_combo(items=["16", "32", "64"], tag="height", default_value="32", width=100)
        with dpg.tooltip("height"):
            dpg.add_text("Select the height of the overworld sprite.")
        
        dpg.add_text("Frames Num", tag="framenum_txt")
        dpg.add_input_int(tag="frame_num", default_value=9, width=100)
        with dpg.tooltip("frame_num"):
            dpg.add_text("Enter the number of frames for the overworld animation.")

    dpg.add_spacer(height=10)
    dpg.add_separator()
    dpg.add_spacer(height=10)
    
    with dpg.collapsing_header(label="Extra Options", tag="extra_options"):
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=60)
            dpg.add_text("Reflection Palette Tag", tag="reflection_palette_txt")
            dpg.add_spacer(width=40)
            dpg.add_text("Palette Slot", tag="palette_slot_txt")
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=50)
            dpg.add_input_text(tag="reflection_palette_tag", default_value="OBJ_EVENT_PAL_TAG_NONE", width=200)
            with dpg.tooltip("reflection_palette_tag"):
                dpg.add_text("Enter the reflection palette tag, or leave as default.")

            dpg.add_combo(items=["PALSLOT_PLAYER", "PALSLOT_NPC_1", "PALSLOT_NPC_2", "PALSLOT_NPC_3", "PALSLOT_NPC_4", "PALSLOT_NPC_5", "PALSLOT_NPC_6", "PALSLOT_NPC_7"], tag="palette_slot", default_value="PALSLOT_NPC_1", width=150)
            with dpg.tooltip("palette_slot"):
                dpg.add_text("Select the palette slot for the overworld.")
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=60)
            dpg.add_text("Anim Table", tag="anim_table_txt")
            dpg.add_spacer(width=90)
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=50)
            dpg.add_combo(items=["QuintyPlump", "Standard", "Following", "Following_Asym", "HoOh", "GroudonSide", "Rayquaza", "BrendanMayNormal", "AcroBike", "Surfing", "Nurse", "FieldMove", "BerryTree", "BreakableRock", "CuttableTree", "Fishing"], tag="anim_table", default_value="Standard", width=180)
            with dpg.tooltip("anim_table"):
                dpg.add_text("Select the Anim Table for the overworld.")
        dpg.add_spacer(height=10)
        dpg.add_separator()
        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=50)
            dpg.add_text("Shadow Size", tag="shadow_size_txt")
            dpg.add_spacer(width=90)
            dpg.add_text("Inanimate", tag="inanimate_txt")
            dpg.add_spacer(width=30)
            dpg.add_text("Tracks", tag="tracks_txt")
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=40)
            dpg.add_combo(items=["SHADOW_SIZE_S", "SHADOW_SIZE_M", "SHADOW_SIZE_L", "SHADOW_SIZE_XL"], tag="shadow_size", default_value="SHADOW_SIZE_M", width=150)
            with dpg.tooltip("shadow_size"):
                dpg.add_text("Select the size of the shadow beneath the overworld.")
            dpg.add_spacer(width=20)
            dpg.add_combo(items=["TRUE", "FALSE"], tag="inanimate", default_value="FALSE", width=100)
            with dpg.tooltip("inanimate"):
                dpg.add_text("Set to TRUE if the overworld should not animate.")
            
            dpg.add_combo( items=["TRUE", "FALSE"], tag="tracks", default_value="FALSE", width=100)
            with dpg.tooltip("tracks"):
                dpg.add_text("Set to TRUE if the overworld should leave tracks when moving.")
    dpg.add_separator()
    with dpg.collapsing_header(label="Pokeemerald Options", tag="pokeemerald_options"):
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=50)
            dpg.add_text("Select Palette Tag (NO DPS)", tag="pal_tag_txt")
            dpg.add_spacer(width=40)
            dpg.add_text("Disable Reflection", tag="disableReflection_txt")
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=50)
            with dpg.tooltip("pal_tag_txt"):
                dpg.add_text("if not using Dynamic Pal System.")
            dpg.add_combo(items=pal_tag_items, tag="pal_tag", default_value="NPC_1", width=180)
            with dpg.tooltip("pal_tag"):
                dpg.add_text("if not using Dynamic Pal System.")
            dpg.add_spacer(width=50)
            dpg.add_combo( items=["TRUE", "FALSE"], tag="disableReflection", default_value="FALSE", width=100)

    dpg.add_spacer(height=15)
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=146)
        dpg.add_button(label="Insert Overworld", callback=insert_overworld_gui, width=200, tag="insert_button")
        with dpg.tooltip("insert_button"):
            dpg.add_text("Click to insert the overworld into the game.")

    dpg.add_text("", tag="status_text")
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=120)
        dpg.add_text("Compatible expansion version: 1.9.0", tag="expansion_ver_txt")

    dpg.add_spacer(height=20)
    dpg.add_text("AOA 0.3.2 By Nexxo", pos=(380, 10))

dpg.bind_theme("purple_theme")

dpg.create_viewport(title='AxoloteOwAdder', width=540, height=590, resizable=False)
dpg.set_primary_window("primary_window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
