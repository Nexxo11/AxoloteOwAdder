import dearpygui.dearpygui as dpg
import json
import os

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

    def toggle_language(self):
        if self.current_language == "en":
            self.current_language = "es"
        else:
            self.current_language = "en"
        self.translations = self.load_translations(self.current_language)
        self.update_texts()

    def update_texts(self):
        dpg.set_item_label('select_folder_button', self.get_text('select_folder_button'))
        dpg.set_value('folder_path_text', self.get_text('folder_path_text'))
        dpg.set_item_label('select_ow_button', self.get_text('select_ow_button'))
        dpg.set_value('sprite_txt_preview', self.get_text('sprite_txt_preview'))
        dpg.set_value('overworld_txt_name', self.get_text('overworld_txt_name'))
        dpg.set_value('width_txt', self.get_text('width_txt'))
        dpg.set_value('height_txt', self.get_text('height_txt'))
        dpg.set_value('framenum_txt', self.get_text('framenum_txt'))
        dpg.set_item_label('extra_options', self.get_text('extra_options'))
        dpg.set_value('reflection_palette_txt', self.get_text('reflection_palette_txt'))
        dpg.set_value('palette_slot_txt', self.get_text('palette_slot_txt'))
        dpg.set_value('anim_table_txt', self.get_text('anim_table_txt'))
        dpg.set_value('shadow_size_txt', self.get_text('shadow_size_txt'))
        dpg.set_value('inanimate_txt', self.get_text('inanimate_txt'))
        dpg.set_value('tracks_txt', self.get_text('tracks_txt'))
        dpg.set_item_label('insert_button', self.get_text('insert_button'))
        dpg.set_value('expansion_ver_txt', self.get_text('expansion_ver_txt'))
        dpg.set_item_label('pokeemerald_options', self.get_text('pokeemerald_options'))
        dpg.set_value('pal_tag_txt', self.get_text('pal_tag_txt'))
        dpg.set_value('disableReflection_txt', self.get_text('disableReflection_txt'))
        dpg.set_value('translate_tooltip_text', self.get_text('translate_tooltip'))
        dpg.set_item_label('translate_button', self.get_text('translate_button'))
