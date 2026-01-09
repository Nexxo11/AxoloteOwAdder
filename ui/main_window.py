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

        setup_themes()
        apply_theme(DEFAULT_THEME_KEY)
        self.setup_main_window()
        setup_popups(self.translator)
        setup_tooltips()

    def setup_main_window(self):
        with dpg.window(tag="primary_window", label="Insert Overworld", width=540, height=580, no_title_bar=True, no_resize=True, no_move=True):
            dpg.add_button(label="Select project Folder", callback=lambda: select_folder(self.translator), tag="select_folder_button")
            dpg.add_text("If you have a path file config, you don't need to load it again", tag="folder_path_text", color=(150, 150, 150))
            # dpg.add_spacer(height=10)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Translate", callback=self.translator.toggle_language, tag="translate_button")
                dpg.add_spacer(width=2)
                dpg.add_button(label="Check for Updates", callback=lambda: verify_version(self.translator), tag="verify_version")
                dpg.add_text("", tag="ver_status_text")

            with dpg.group(horizontal=True):
                dpg.add_spacer(width=300)
                dpg.add_text(self.translator.get_text("theme_label"), tag="theme_label")

                def _on_theme_change(sender, app_data):
                    theme_map = {
                        self.translator.get_text("theme_purple"): "purple",
                        self.translator.get_text("theme_light"): "light",
                    }
                    theme_key = theme_map.get(app_data, DEFAULT_THEME_KEY)
                    dpg.set_item_user_data("theme_select", {"theme_key": theme_key})
                    apply_theme(theme_key)

                theme_items = [
                    self.translator.get_text("theme_purple"),
                    self.translator.get_text("theme_light"),
                ]
                default_theme_display = self.translator.get_text(get_theme_label_key(DEFAULT_THEME_KEY))
                dpg.add_combo(
                    items=theme_items,
                    tag="theme_select",
                    default_value=default_theme_display,
                    width=120,
                    callback=_on_theme_change,
                )
                dpg.set_item_user_data("theme_select", {"theme_key": DEFAULT_THEME_KEY})
            
            dpg.add_text("", tag="footer_text", pos=(380, 10))
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=142)
                dpg.add_button(label="Select new overworld to add", callback=lambda: select_and_move_sprite(self.translator), tag="select_ow_button")
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=100)
                dpg.add_text("Sprite Preview", tag="sprite_txt_preview", color=(150, 150, 150))
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=96)
                with dpg.child_window(tag="sprite_preview", width=300, height=64, border=True):
                    dpg.add_text(tag="preview_text")
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=156)
                dpg.add_text("Overworld Name", tag="overworld_txt_name")
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=146)
                dpg.add_input_text(tag="overworld_name", width=200)

            dpg.add_spacer(height=5)
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=146)
                
                def _update_name_from_combo(sender, app_data):
                    dpg.set_value("overworld_name", app_data)

                def _refresh_overworld_list():
                    ows = get_custom_overworlds()
                    dpg.configure_item("installed_overworlds_combo", items=ows)
                    # dpg.set_value("status_text", "Overworld list refreshed.")

                dpg.add_combo(items=[], tag="installed_overworlds_combo", width=170, callback=_update_name_from_combo, default_value="Select Installed...")
                dpg.add_button(label="🔄", width=30, callback=_refresh_overworld_list, tag="refresh_list_btn")
            
            # Initial load attempt (will only work if path is already set)
            try:
                _refresh_overworld_list()
            except:
                pass

            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            with dpg.group(horizontal=True):
                dpg.add_text("Width", tag="width_txt")
                dpg.add_combo(items=["16", "32", "64"], tag="width", default_value="32", width=100)
                
                dpg.add_text("Height", tag="height_txt")
                dpg.add_combo(items=["16", "32", "64"], tag="height", default_value="32", width=100)
                
                dpg.add_text("Frames Num", tag="framenum_txt")
                dpg.add_input_int(tag="frame_num", default_value=9, width=100)

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

                    dpg.add_combo(items=["PALSLOT_PLAYER", "PALSLOT_NPC_1", "PALSLOT_NPC_2", "PALSLOT_NPC_3", "PALSLOT_NPC_4", "PALSLOT_NPC_5", "PALSLOT_NPC_6", "PALSLOT_NPC_7"], tag="palette_slot", default_value="PALSLOT_NPC_1", width=150)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=60)
                    dpg.add_text("Anim Table", tag="anim_table_txt")
                    dpg.add_spacer(width=90)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=50)
                    dpg.add_combo(items=["QuintyPlump", "Standard", "Following", "Following_Asym", "HoOh", "GroudonSide", "Rayquaza", "BrendanMayNormal", "AcroBike", "Surfing", "Nurse", "FieldMove", "BerryTree", "BreakableRock", "CuttableTree", "Fishing"], tag="anim_table", default_value="Standard", width=180)
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
                    dpg.add_spacer(width=20)
                    dpg.add_combo(items=["TRUE", "FALSE"], tag="inanimate", default_value="FALSE", width=100)
                    
                    dpg.add_combo( items=["TRUE", "FALSE"], tag="tracks", default_value="FALSE", width=100)
            dpg.add_separator()
            with dpg.collapsing_header(label="Pokeemerald Options", tag="pokeemerald_options"):
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=50)
                    dpg.add_text("Select Palette Tag (NO DPS)", tag="pal_tag_txt")
                    dpg.add_spacer(width=40)
                    dpg.add_text("Disable Reflection", tag="disableReflection_txt")
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=50)
                    dpg.add_combo(items=self.pal_tag_items, tag="pal_tag", default_value="NPC_1", width=180)
                    dpg.add_spacer(width=50)
                    dpg.add_combo( items=["TRUE", "FALSE"], tag="disableReflection", default_value="FALSE", width=100)

            dpg.add_spacer(height=15)
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=50)
                dpg.add_button(label="Insert Overworld", callback=lambda: insert_overworld_gui(self.translator), width=200, tag="insert_button")
                dpg.add_spacer(width=10)
                dpg.add_button(label="Delete Overworld", callback=lambda: show_delete_confirmation(self.translator), width=200, tag="delete_button")

            dpg.add_separator()
            with dpg.group(tag="status_panel"):
                dpg.add_text("", tag="status_text")
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=120)
                dpg.add_text("Compatible expansion version: 1.13.1", tag="expansion_ver_txt")

            dpg.add_spacer(height=20)
            dpg.add_text("AOA 0.4.1 By Nexxo", pos=(380, 10))
