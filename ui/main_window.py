import dearpygui.dearpygui as dpg
from core.adder import insert_overworld_gui, get_custom_overworlds
from core.config import select_folder
from core.sprite import select_and_move_sprite
from core.version import verify_version
from .themes import setup_themes, apply_theme, DEFAULT_THEME_KEY, get_theme_label_key
from .popups import setup_popups, show_delete_confirmation
from .tooltips import setup_tooltips

class MainWindow:
    def __init__(self, translator):
        self.translator = translator
        self.pal_tag_items = [
            "BRENDAN", "BRENDAN_REFLECTION", "BRIDGE_REFLECTION", "NPC_1", "NPC_2", "NPC_3", "NPC_4",
            "NPC_1_REFLECTION", "NPC_2_REFLECTION", "NPC_3_REFLECTION", "NPC_4_REFLECTION",
            "QUINTY_PLUMP", "QUINTY_PLUMP_REFLECTION", "TRUCK", "VIGOROTH", "ZIGZAGOON", "MAY",
            "MAY_REFLECTION", "MOVING_BOX", "CABLE_CAR", "SSTIDAL", "PLAYER_UNDERWATER", "KYOGRE",
            "KYOGRE_REFLECTION", "GROUDON", "GROUDON_REFLECTION", "UNUSED", "SUBMARINE_SHADOW",
            "POOCHYENA", "RED_LEAF", "DEOXYS", "BIRTH_ISLAND_STONE", "HO_OH", "LUGIA", "RS_BRENDAN",
            "RS_MAY", "NONE"
        ]

        setup_themes()
        apply_theme(DEFAULT_THEME_KEY)
        self.setup_main_window()
        setup_popups(self.translator)
        setup_tooltips()

    def setup_main_window(self):
        with dpg.window(tag="primary_window", label="Insert Overworld", width=540, height=720, 
                       no_title_bar=True, no_resize=True, no_move=True):
            
            # --- Hidden Data Fields (Proxy for Logic Compatibility with core/adder.py) ---
            # core/adder.py reads these tags and expects "TRUE"/"FALSE" strings.
            dpg.add_input_text(tag="inanimate", default_value="FALSE", show=False)
            dpg.add_input_text(tag="tracks", default_value="FALSE", show=False)
            dpg.add_input_text(tag="disableReflection", default_value="FALSE", show=False)

            def _sync_bool(sender, app_data, user_data):
                dpg.set_value(user_data, "TRUE" if app_data else "FALSE")

            # --- Menu Bar ---
            with dpg.menu_bar():
                with dpg.menu(label="Settings"):
                    dpg.add_menu_item(label="Toggle Language", callback=self.translator.toggle_language, tag="translate_button")
                    
                    with dpg.menu(label="Theme"):
                        def _on_theme_change(sender, app_data, user_data):
                            apply_theme(user_data)
                            
                        dpg.add_menu_item(label=self.translator.get_text("theme_purple"), callback=_on_theme_change, user_data="purple")
                        dpg.add_menu_item(label=self.translator.get_text("theme_light"), callback=_on_theme_change, user_data="light")

                with dpg.menu(label="Help"):
                    dpg.add_menu_item(label="Check for Updates", callback=lambda: verify_version(self.translator), tag="verify_version")

            # --- 1. Project / Setup ---
            dpg.add_text("Project Setup", color=(150, 150, 150))
            dpg.add_separator()
            dpg.add_spacer(height=5)
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="Select Project Folder", callback=lambda: select_folder(self.translator), tag="select_folder_button", width=160)
                dpg.add_text("No folder selected", tag="folder_path_text", color=(200, 200, 200), wrap=340) 
            
            dpg.add_text("", tag="ver_status_text")
            dpg.add_spacer(height=5)

            # --- 2. Overworld Management ---
            dpg.add_text("Overworld Management", color=(150, 150, 150))
            dpg.add_separator()
            dpg.add_spacer(height=5)
            
            # Main Action: Select Source
            dpg.add_button(label="Select Source Image (Sprite)", callback=lambda: select_and_move_sprite(self.translator), tag="select_ow_button", width=-1, height=30)
            dpg.add_spacer(height=10)
            
            # Name and Reference in a grid-like structure
            with dpg.group():
                dpg.add_text("Overworld Name", tag="overworld_txt_name")
                
                with dpg.group(horizontal=True):
                    dpg.add_input_text(tag="overworld_name", width=250)
                    
                    # Reference / Install Check
                    dpg.add_spacer(width=20)
                    
                    def _update_name_from_combo(sender, app_data):
                        dpg.set_value("overworld_name", app_data)

                    def _refresh_overworld_list():
                        ows = get_custom_overworlds()
                        dpg.configure_item("installed_overworlds_combo", items=ows)

                    with dpg.group():
                         # Use a small group for the combo + refresh to align them
                         with dpg.group(horizontal=True):
                            dpg.add_combo(items=[], tag="installed_overworlds_combo", width=180, callback=_update_name_from_combo, default_value="Select Installed...")
                            dpg.add_button(label="R", width=30, callback=_refresh_overworld_list, tag="refresh_list_btn")
                            with dpg.tooltip("refresh_list_btn"):
                                dpg.add_text("Refresh List")

            # --- 3. Sprite Specifications ---
            dpg.add_spacer(height=10)
            dpg.add_text("Sprite Specifications", color=(150, 150, 150))
            dpg.add_separator()
            dpg.add_spacer(height=5)
            
            with dpg.group(horizontal=True):
                # Distribute evenly
                with dpg.group():
                    dpg.add_text("Width", tag="width_txt")
                    dpg.add_combo(items=["16", "32", "64"], tag="width", default_value="32", width=120)
                
                dpg.add_spacer(width=30)
                with dpg.group():
                    dpg.add_text("Height", tag="height_txt")
                    dpg.add_combo(items=["16", "32", "64"], tag="height", default_value="32", width=120)
                
                dpg.add_spacer(width=30)
                with dpg.group():
                    dpg.add_text("Frames", tag="framenum_txt")
                    dpg.add_input_int(tag="frame_num", default_value=9, width=120)

            # --- 4. Advanced Options ---
            dpg.add_spacer(height=10)
            with dpg.collapsing_header(label="Advanced Options", tag="extra_options"):
                
                dpg.add_text("Palette & Animations", color=(255, 200, 100))
                with dpg.group(horizontal=True):
                    with dpg.group():
                        dpg.add_text("Palette Slot", tag="palette_slot_txt")
                        dpg.add_combo(items=["PALSLOT_PLAYER", "PALSLOT_NPC_1", "PALSLOT_NPC_2", "PALSLOT_NPC_3", "PALSLOT_NPC_4", "PALSLOT_NPC_5", "PALSLOT_NPC_6", "PALSLOT_NPC_7"], tag="palette_slot", default_value="PALSLOT_NPC_1", width=180)
                    
                    dpg.add_spacer(width=20)
                    with dpg.group():
                        dpg.add_text("Anim Table", tag="anim_table_txt")
                        dpg.add_combo(items=["QuintyPlump", "Standard", "Following", "Following_Asym", "HoOh", "GroudonSide", "Rayquaza", "BrendanMayNormal", "AcroBike", "Surfing", "Nurse", "FieldMove", "BerryTree", "BreakableRock", "CuttableTree", "Fishing"], tag="anim_table", default_value="Standard", width=180)

                dpg.add_spacer(height=5)
                with dpg.group(horizontal=True):
                    with dpg.group():
                         dpg.add_text("Refl. Pal Tag", tag="reflection_palette_txt")
                         dpg.add_input_text(tag="reflection_palette_tag", default_value="OBJ_EVENT_PAL_TAG_NONE", width=180)

                dpg.add_spacer(height=10)
                dpg.add_text("Properties", color=(255, 200, 100))
                with dpg.group(horizontal=True):
                    with dpg.group():
                        dpg.add_text("Shadow Size", tag="shadow_size_txt")
                        dpg.add_combo(items=["SHADOW_SIZE_S", "SHADOW_SIZE_M", "SHADOW_SIZE_L", "SHADOW_SIZE_XL"], tag="shadow_size", default_value="SHADOW_SIZE_M", width=150)
                    
                    dpg.add_spacer(width=20)
                    dpg.add_checkbox(label="Inanimate", callback=_sync_bool, user_data="inanimate", default_value=False, tag="chk_inanimate")
                    dpg.add_spacer(width=10)
                    dpg.add_checkbox(label="Tracks", callback=_sync_bool, user_data="tracks", default_value=False, tag="chk_tracks")
                
                dpg.add_spacer(height=10)
                dpg.add_text("Pokeemerald Specifics", tag="pokeemerald_options", color=(255, 200, 100))
                with dpg.group(horizontal=True):
                    with dpg.group():
                        dpg.add_text("Pal Tag (NO DPS)", tag="pal_tag_txt")
                        dpg.add_combo(items=self.pal_tag_items, tag="pal_tag", default_value="NPC_1", width=180)
                    dpg.add_spacer(width=20)
                    dpg.add_checkbox(label="Disable Reflection", callback=_sync_bool, user_data="disableReflection", default_value=False, tag="chk_disableReflection")

            # --- 5. Actions ---
            dpg.add_spacer(height=15)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            dpg.add_button(label="INSERT OVERWORLD", callback=lambda: insert_overworld_gui(self.translator), width=-1, height=45, tag="insert_button")
            
            dpg.add_spacer(height=5)
            dpg.add_button(label="Delete Selected Overworld", callback=lambda: show_delete_confirmation(self.translator), width=-1, tag="delete_button")

            # --- Status & Footer ---
            dpg.add_spacer(height=10)
            dpg.add_separator()
            with dpg.group(tag="status_panel"):
                 dpg.add_text("", tag="status_text")
            
            with dpg.group(horizontal=True):
                dpg.add_text("Compatible expansion version: 1.13.1", tag="expansion_ver_txt", color=(100, 100, 100))
                dpg.add_spacer(width=100)
                dpg.add_text("AOA 0.4.1 By Nexxo", color=(100,100,100))

            # Initial load attempt
            try:
                _refresh_overworld_list()
            except:
                pass