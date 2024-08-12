import dearpygui.dearpygui as dpg
import json
import os

def load_translations(language):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to translate.json
    json_path = os.path.join(script_dir, 'translate.json')
    
    # Load the JSON file
    with open(json_path, 'r', encoding='utf-8') as file:
        translations = json.load(file)
    
    return translations.get(language, {})

current_language = "en"
translations = load_translations(current_language)

def get_text(key):
    return translations.get(key, f"[Missing translation for {key}]")

def change_language(sender, app_data):
    global current_language
    current_language = app_data
    update_texts()

def update_texts():
    print("Updating texts...")
    dpg.set_item_label('select_folder_button', get_text('select_folder_button'))
    dpg.set_value('folder_path_text', get_text('folder_path_text'))
    dpg.set_item_label('select_ow_button', get_text('select_ow_button'))
    dpg.set_value('sprite_txt_preview', get_text('sprite_txt_preview'))
    dpg.set_value('overworld_txt_name', get_text('overworld_txt_name'))
    dpg.set_value('width_txt', get_text('width_txt'))
    dpg.set_value('height_txt', get_text('height_txt'))
    dpg.set_value('framenum_txt', get_text('framenum_txt'))
    dpg.set_item_label('extra_options', get_text('extra_options'))
    dpg.set_value('reflection_palette_txt', get_text('reflection_palette_txt'))
    dpg.set_value('palette_slot_txt', get_text('palette_slot_txt'))
    dpg.set_value('anim_table_txt', get_text('anim_table_txt'))
    dpg.set_value('shadow_size_txt', get_text('shadow_size_txt'))
    dpg.set_value('inanimate_txt', get_text('inanimate_txt'))
    dpg.set_value('tracks_txt', get_text('tracks_txt'))
    dpg.set_item_label('insert_button', get_text('insert_button'))
    dpg.set_value('expansion_ver_txt', get_text('expansion_ver_txt'))
