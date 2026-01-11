import dearpygui.dearpygui as dpg
from core.adder import insert_overworld_gui, get_custom_overworlds, restore_backups
from core.config import select_folder
from core.sprite import select_and_move_sprite
from core.version import verify_version, check_project_compatibility
from .themes import (
    setup_themes,
    apply_theme,
    DEFAULT_THEME_KEY,
    get_theme_label_key,
    get_primary_button_theme_tag,
    get_danger_button_theme_tag,
)
from .popups import setup_popups, show_delete_confirmation
from .tooltips import setup_tooltips
from utils.icons import register_icon
import os
import configparser


class MainWindow:
    def __init__(self, translator):
        self.translator = translator

        self.current_theme_key = DEFAULT_THEME_KEY  # track current theme
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
        apply_theme(self.current_theme_key)

        # Icons
        self.refresh_icon_tag = "icon_refresh"
        icon_path = os.path.join("assets", "refresh.png")
        self.has_refresh_icon = register_icon(icon_path, self.refresh_icon_tag)

        self.setup_main_window()
        setup_popups(self.translator)
        setup_tooltips()

    def _bind_action_button_themes(self):
        """Bind per-item themes for primary/danger buttons based on current theme."""
        dpg.bind_item_theme("insert_button", get_primary_button_theme_tag(self.current_theme_key))
        dpg.bind_item_theme("delete_button", get_danger_button_theme_tag(self.current_theme_key))

    def setup_main_window(self):
        with dpg.window(
            tag="primary_window",
            label="AxoloteOwAdder",
            width=560,
            height=720,
        ):
            # --- Hidden Data Fields (required by core/adder.py) ---
            dpg.add_input_text(tag="inanimate", default_value="FALSE", show=False)
            dpg.add_input_text(tag="tracks", default_value="FALSE", show=False)
            dpg.add_input_text(tag="disableReflection", default_value="FALSE", show=False)

            def _sync_bool(sender, app_data, user_data):
                dpg.set_value(user_data, "TRUE" if app_data else "FALSE")

            # --- Helpers ---
            def _update_name_from_combo(sender, app_data):
                dpg.set_value("overworld_name", app_data)

            def _refresh_overworld_list():
                ows = get_custom_overworlds()
                if ows is not None:
                    dpg.configure_item("installed_overworlds_combo", items=ows)

            def _on_theme_change(sender, app_data, user_data):
                self.current_theme_key = user_data
                apply_theme(user_data)
                self._bind_action_button_themes()

            # Small spacing helpers (consistent + easy to tweak)
            def vspace(px=4):
                dpg.add_spacer(height=px)

            # =========================
            # Menu Bar
            # =========================
            with dpg.menu_bar():
                with dpg.menu(label=self.translator.get_text("menu_settings"), tag="menu_settings"):
                    with dpg.menu(label=self.translator.get_text("menu_language"), tag="menu_language"):
                        dpg.add_menu_item(label=self.translator.get_text("lang_en"), callback=lambda: self.translator.set_language("en"), tag="lang_en")
                        dpg.add_menu_item(label=self.translator.get_text("lang_es"), callback=lambda: self.translator.set_language("es"), tag="lang_es")
                        dpg.add_menu_item(label=self.translator.get_text("lang_pt"), callback=lambda: self.translator.set_language("pt"), tag="lang_pt")
                        dpg.add_menu_item(label=self.translator.get_text("lang_fr"), callback=lambda: self.translator.set_language("fr"), tag="lang_fr")
                    with dpg.menu(label=self.translator.get_text("menu_theme"), tag="menu_theme"):
                        dpg.add_menu_item(
                            label=self.translator.get_text("theme_purple"),
                            callback=_on_theme_change,
                            user_data="purple",
                            tag="theme_purple_item"
                        )
                        dpg.add_menu_item(
                            label=self.translator.get_text("theme_light"),
                            callback=_on_theme_change,
                            user_data="light",
                            tag="theme_light_item"
                        )
                    dpg.add_menu_item(
                        label=self.translator.get_text("menu_restore_backups"),
                        callback=lambda: restore_backups(self.translator),
                        tag="restore_backups_button",
                    )

                with dpg.menu(label=self.translator.get_text("menu_help"), tag="menu_help"):
                    dpg.add_menu_item(
                        label=self.translator.get_text("menu_check_updates"),
                        callback=lambda: verify_version(self.translator),
                        tag="verify_version",
                    )

            # =========================
            # Project Setup
            # =========================
            vspace(4)
            dpg.add_text(self.translator.get_text("header_project_setup"), tag="header_project_setup", color=(120, 130, 145))
            dpg.add_separator()
            # vspace(4)

            with dpg.group(horizontal=True):
                dpg.add_button(
                    label=self.translator.get_text("select_folder_button"),
                    callback=lambda: select_folder(self.translator),
                    tag="select_folder_button",
                    width=-1,
                    height=32,
                )
            # dpg.add_spacer(width=10)
            dpg.add_text(self.translator.get_text("text_no_folder"), tag="folder_path_text", color=(150, 160, 175))

            # vspace(2)
            dpg.add_text("", tag="ver_status_text")

            # =========================
            # Overworld
            # =========================
            # vspace(8)
            dpg.add_text(self.translator.get_text("header_overworld"), tag="header_overworld", color=(120, 130, 145))
            dpg.add_separator()
            vspace(2)

            dpg.add_button(
                label=self.translator.get_text("select_ow_button"),
                callback=lambda: select_and_move_sprite(self.translator),
                tag="select_ow_button",
                width=-1,
                height=34,
            )

            vspace(4)
            
            with dpg.group():
                dpg.add_text(self.translator.get_text("overworld_txt_name"), tag="overworld_txt_name", color=(140, 150, 165))
                dpg.add_input_text(tag="overworld_name", width=-1)

            vspace(2)

            with dpg.group():
                dpg.add_text(self.translator.get_text("text_installed"), tag="text_installed", color=(140, 150, 165))
                with dpg.group(horizontal=True):
                    dpg.add_combo(
                        items=[],
                        tag="installed_overworlds_combo",
                        width=-50,
                        callback=_update_name_from_combo,
                        default_value="Select...",
                    )
                    # dpg.add_spacer(width=4)
                    if self.has_refresh_icon:
                        dpg.add_image_button(
                            texture_tag=self.refresh_icon_tag,
                            width=22,
                            height=22,
                            callback=_refresh_overworld_list,
                            tag="refresh_list_btn",
                        )
                    else:
                        dpg.add_button(
                            label="↻",
                            width=36,
                            height=30,
                            callback=_refresh_overworld_list,
                            tag="refresh_list_btn",
                        )
            # =========================
            # Sprite Settings
            # =========================
            vspace(6)
            dpg.add_text(self.translator.get_text("header_sprite_settings"), tag="header_sprite_settings", color=(120, 130, 145))
            dpg.add_separator()
            vspace(2)

            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()

                with dpg.table_row():
                    with dpg.group():
                        dpg.add_text(self.translator.get_text("width_txt"), tag="width_txt", color=(140, 150, 165))
                        dpg.add_combo(items=["16", "32", "64"], tag="width", default_value="32", width=-1)

                    with dpg.group():
                        dpg.add_text(self.translator.get_text("height_txt"), tag="height_txt", color=(140, 150, 165))
                        dpg.add_combo(items=["16", "32", "64"], tag="height", default_value="32", width=-1)

                    with dpg.group():
                        dpg.add_text(self.translator.get_text("framenum_txt"), tag="framenum_txt", color=(140, 150, 165))
                        dpg.add_input_int(tag="frame_num", default_value=9, width=-1)

            # =========================
            # Advanced Options
            # =========================
            vspace(6)
            with dpg.collapsing_header(label=self.translator.get_text("extra_options"), tag="extra_options", default_open=False):
                dpg.add_text(self.translator.get_text("header_palette_anim"), tag="header_palette_anim", color=(120, 130, 145))
                dpg.add_separator()
                vspace(2)

                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    with dpg.table_row():
                        with dpg.group():
                            dpg.add_text(self.translator.get_text("palette_slot_txt"), tag="palette_slot_txt", color=(140, 150, 165))
                            dpg.add_combo(
                                items=[
                                    "PALSLOT_PLAYER", "PALSLOT_NPC_1", "PALSLOT_NPC_2",
                                    "PALSLOT_NPC_3", "PALSLOT_NPC_4", "PALSLOT_NPC_5",
                                    "PALSLOT_NPC_6", "PALSLOT_NPC_7",
                                ],
                                tag="palette_slot",
                                default_value="PALSLOT_NPC_1",
                                width=-1,
                            )
                        with dpg.group():
                            dpg.add_text(self.translator.get_text("anim_table_txt"), tag="anim_table_txt", color=(140, 150, 165))
                            dpg.add_combo(
                                items=[
                                    "QuintyPlump", "Standard", "Following", "Following_Asym",
                                    "HoOh", "GroudonSide", "Rayquaza", "BrendanMayNormal",
                                    "AcroBike", "Surfing", "Nurse", "FieldMove", "BerryTree",
                                    "BreakableRock", "CuttableTree", "Fishing",
                                ],
                                tag="anim_table",
                                default_value="Standard",
                                width=-1,
                            )

                vspace(4)
                dpg.add_text(self.translator.get_text("reflection_palette_txt"), tag="reflection_palette_txt", color=(140, 150, 165))
                dpg.add_input_text(
                    tag="reflection_palette_tag",
                    default_value="OBJ_EVENT_PAL_TAG_NONE",
                    width=-1,
                )

                vspace(6)
                dpg.add_text(self.translator.get_text("header_properties"), tag="header_properties", color=(120, 130, 145))
                dpg.add_separator()
                vspace(2)

                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    with dpg.table_row():
                        with dpg.group():
                            dpg.add_text(self.translator.get_text("shadow_size_txt"), tag="shadow_size_txt", color=(140, 150, 165))
                            dpg.add_combo(
                                items=["SHADOW_SIZE_S", "SHADOW_SIZE_M", "SHADOW_SIZE_L", "SHADOW_SIZE_XL"],
                                tag="shadow_size",
                                default_value="SHADOW_SIZE_M",
                                width=-1,
                            )
                        with dpg.group(horizontal=True):
                            # dpg.add_spacer(width=10)
                            dpg.add_checkbox(label=self.translator.get_text("inanimate_txt"), callback=_sync_bool, user_data="inanimate", tag="chk_inanimate")
                            dpg.add_spacer(width=6)
                            dpg.add_checkbox(label=self.translator.get_text("tracks_txt"), callback=_sync_bool, user_data="tracks", tag="chk_tracks")

                vspace(6)
                dpg.add_text(self.translator.get_text("pokeemerald_options"), tag="pokeemerald_options", color=(120, 130, 145))
                dpg.add_separator()
                vspace(2)

                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    with dpg.table_row():
                        with dpg.group():
                            dpg.add_text(self.translator.get_text("pal_tag_txt"), tag="pal_tag_txt", color=(140, 150, 165))
                            dpg.add_combo(
                                items=self.pal_tag_items,
                                tag="pal_tag",
                                default_value="NPC_1",
                                width=-1,
                            )
                        with dpg.group():
                            # dpg.add_spacer(width=10)
                            dpg.add_checkbox(
                                label=self.translator.get_text("disableReflection_txt"),
                                callback=_sync_bool,
                                user_data="disableReflection",
                                tag="chk_disableReflection",
                            )

            def _on_insert():
                insert_overworld_gui(self.translator)
                _refresh_overworld_list()

            # =========================
            # Actions
            # =========================
            vspace(8)
            dpg.add_separator()
            vspace(4)

            dpg.add_button(
                label=self.translator.get_text("insert_button"),
                callback=_on_insert,
                width=-1,
                height=44,
                tag="insert_button",
            )

            vspace(4)
            dpg.add_button(
                label=self.translator.get_text("delete_button"),
                callback=lambda: show_delete_confirmation(self.translator, callback=_refresh_overworld_list),
                width=-1,
                height=38,
                tag="delete_button",
            )

            vspace(2)
            dpg.add_text("", tag="status_text", wrap=540)

            # =========================
            # Footer
            # =========================
            vspace(6)
            dpg.add_separator()
            vspace(4)

            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_text(self.translator.get_text("expansion_ver_txt"), tag="expansion_ver_txt", color=(120, 130, 145))
                    dpg.add_text(self.translator.get_text("text_credits"), tag="text_credits", color=(120, 130, 145), indent=100)

            # Initial load
            try:
                config = configparser.ConfigParser()
                config.read('path.ini')
                if config.has_section('pkmn_path') and 'path' in config['pkmn_path']:
                    saved_path = config['pkmn_path']['path']
                    if saved_path:
                        dpg.set_value("folder_path_text", f"{self.translator.get_text('selected_path')}{saved_path}")
                        check_project_compatibility(saved_path, self.translator)
                
                _refresh_overworld_list()
            except Exception as e:
                print(f"Error during initial load: {e}")

            self._bind_action_button_themes()
