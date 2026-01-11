import dearpygui.dearpygui as dpg
import json
import os
from ui.themes import DEFAULT_THEME_KEY, get_theme_label_key

class Translator:
    def __init__(self):
        self.current_language = "en"
        self.translations = self.load_translations(self.current_language)

    def load_translations(self, language):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, f'{language}.json')
        with open(json_path, 'r', encoding='utf-8') as file:
            translations = json.load(file)
        
        return translations

    def get_text(self, key):
        return self.translations.get(key, f"[Missing translation for {key}]")

    def set_language(self, language_code):
        self.current_language = language_code
        self.translations = self.load_translations(self.current_language)
        self.update_texts()

    def update_texts(self):
        # Menu
        if dpg.does_item_exist("menu_settings"): dpg.set_item_label('menu_settings', self.get_text('menu_settings'))
        if dpg.does_item_exist("menu_language"): dpg.set_item_label('menu_language', self.get_text('menu_language'))
        if dpg.does_item_exist("lang_en"): dpg.set_item_label('lang_en', self.get_text('lang_en'))
        if dpg.does_item_exist("lang_es"): dpg.set_item_label('lang_es', self.get_text('lang_es'))
        if dpg.does_item_exist("lang_pt"): dpg.set_item_label('lang_pt', self.get_text('lang_pt'))
        if dpg.does_item_exist("menu_theme"): dpg.set_item_label('menu_theme', self.get_text('menu_theme'))
        if dpg.does_item_exist("restore_backups_button"): dpg.set_item_label('restore_backups_button', self.get_text('menu_restore_backups'))
        if dpg.does_item_exist("menu_help"): dpg.set_item_label('menu_help', self.get_text('menu_help'))
        if dpg.does_item_exist("verify_version"): dpg.set_item_label('verify_version', self.get_text('menu_check_updates'))
        if dpg.does_item_exist("theme_purple_item"): dpg.set_item_label('theme_purple_item', self.get_text('theme_purple'))
        if dpg.does_item_exist("theme_light_item"): dpg.set_item_label('theme_light_item', self.get_text('theme_light'))

        # Project Setup
        if dpg.does_item_exist("header_project_setup"): dpg.set_value('header_project_setup', self.get_text('header_project_setup'))
        dpg.set_item_label('select_folder_button', self.get_text('select_folder_button'))
        if dpg.does_item_exist("folder_path_text") and dpg.get_value("folder_path_text") in [self.get_text("text_no_folder") for self.get_text in [lambda k: self.translations.get(k)]]:
             # Only update if it still says "No folder selected" (in any lang). 
             # Logic simplified: just check if it matches the 'text_no_folder' of the *previous* lang? 
             # Actually, simpler: if the user hasn't selected a folder, it shows the "No folder" text.
             # We can just update it if the current value matches a known "No folder" string.
             # For now, let's just update it. If it holds a path, we shouldn't overwrite it.
             current_val = dpg.get_value("folder_path_text")
             if "Users" not in current_val and ":\\" not in current_val and "/" not in current_val: # Simple heuristic
                 dpg.set_value('folder_path_text', self.get_text('text_no_folder'))

        # Overworld
        if dpg.does_item_exist("header_overworld"): dpg.set_value('header_overworld', self.get_text('header_overworld'))
        dpg.set_item_label('select_ow_button', self.get_text('select_ow_button'))
        dpg.set_value('overworld_txt_name', self.get_text('overworld_txt_name'))
        if dpg.does_item_exist("text_installed"): dpg.set_value('text_installed', self.get_text('text_installed'))

        # Sprite Settings
        if dpg.does_item_exist("header_sprite_settings"): dpg.set_value('header_sprite_settings', self.get_text('header_sprite_settings'))
        dpg.set_value('width_txt', self.get_text('width_txt'))
        dpg.set_value('height_txt', self.get_text('height_txt'))
        dpg.set_value('framenum_txt', self.get_text('framenum_txt'))

        # Advanced
        dpg.set_item_label('extra_options', self.get_text('extra_options'))
        if dpg.does_item_exist("header_palette_anim"): dpg.set_value('header_palette_anim', self.get_text('header_palette_anim'))
        dpg.set_value('palette_slot_txt', self.get_text('palette_slot_txt'))
        dpg.set_value('anim_table_txt', self.get_text('anim_table_txt'))
        dpg.set_value('reflection_palette_txt', self.get_text('reflection_palette_txt'))
        if dpg.does_item_exist("header_properties"): dpg.set_value('header_properties', self.get_text('header_properties'))
        dpg.set_value('shadow_size_txt', self.get_text('shadow_size_txt'))
        if dpg.does_item_exist("chk_inanimate"):
            dpg.set_item_label('chk_inanimate', self.get_text('inanimate_txt'))
        if dpg.does_item_exist("chk_tracks"):
            dpg.set_item_label('chk_tracks', self.get_text('tracks_txt'))
        
        dpg.set_value('pokeemerald_options', self.get_text('pokeemerald_options'))
        dpg.set_value('pal_tag_txt', self.get_text('pal_tag_txt'))
        if dpg.does_item_exist("chk_disableReflection"):
            dpg.set_item_label('chk_disableReflection', self.get_text('disableReflection_txt'))
        
        # Actions
        dpg.set_item_label('insert_button', self.get_text('insert_button'))
        dpg.set_item_label('delete_button', self.get_text('delete_button'))
        
        # Footer
        dpg.set_value('expansion_ver_txt', self.get_text('expansion_ver_txt'))
        if dpg.does_item_exist("text_credits"): dpg.set_value('text_credits', self.get_text('text_credits'))

        # Tooltips
        dpg.set_value('translate_tooltip_text', self.get_text('translate_tooltip'))
        if dpg.does_item_exist("refresh_tooltip_text"):
            dpg.set_value('refresh_tooltip_text', self.get_text('refresh_tooltip'))
        if dpg.does_item_exist("theme_label"):
            dpg.set_value("theme_label", self.get_text("theme_label"))
        if dpg.does_item_exist("theme_select"):
            user_data = dpg.get_item_user_data("theme_select")
            theme_key = DEFAULT_THEME_KEY
            if isinstance(user_data, dict) and "theme_key" in user_data:
                theme_key = user_data["theme_key"]
            dpg.configure_item(
                "theme_select",
                items=[self.get_text("theme_purple"), self.get_text("theme_light")],
            )
            dpg.set_value("theme_select", self.get_text(get_theme_label_key(theme_key)))
