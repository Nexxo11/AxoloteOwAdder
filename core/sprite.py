import configparser
import tkinter as tk
from tkinter import filedialog
import dearpygui.dearpygui as dpg
import os
import shutil

config = configparser.ConfigParser()
config.read('path.ini')

def select_and_move_sprite(translator):
    root = tk.Tk()
    root.withdraw()
    sprite_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*")])

    if sprite_path:
        if dpg.does_item_exist("sprite_image"):
            dpg.delete_item("sprite_image")
        if dpg.does_item_exist("sprite_texture"):
            dpg.delete_item("sprite_texture")

        config = configparser.ConfigParser()
        config.read('path.ini')
        
        if 'pkmn_path' in config and 'path' in config['pkmn_path']:
            destination_folder = os.path.join(config['pkmn_path']['path'], "graphics/object_events/pics/people/")
            
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            destination_path = os.path.join(destination_folder, os.path.basename(sprite_path))
            shutil.move(sprite_path, destination_path)

            if os.path.exists(destination_path):
                try:
                    width, height, channels, data = dpg.load_image(destination_path)
                    preview_width = dpg.get_item_width("sprite_preview")
                    preview_height = dpg.get_item_height("sprite_preview")

                    pos_x = (preview_width - width) / 2 if width < preview_width else 0
                    pos_y = (preview_height - height) / 2 if height < preview_height else 0

                    if dpg.does_item_exist("sprite_image"):
                        dpg.delete_item("sprite_image")

                    with dpg.texture_registry(show=False):
                        dpg.add_static_texture(width, height, data, tag="sprite_texture")

                    dpg.add_image("sprite_texture", parent="sprite_preview", tag="sprite_image", pos=(pos_x, pos_y))
                    dpg.set_value("status_text", translator.get_text('sprite_moved'))
                except Exception as e:
                    dpg.set_value("status_text", f"{translator.get_text('error_displaying_sprite')}{str(e)}")
            else:
                dpg.set_value("status_text", translator.get_text('error_displaying_sprite_not_found'))
        else:
            dpg.set_value("status_text", translator.get_text('destination_folder_not_set'))
    else:
        dpg.set_value("status_text", translator.get_text('no_sprite_selected'))
