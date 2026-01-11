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

        config = configparser.ConfigParser()
        config.read('path.ini')
        
        if 'pkmn_path' in config and 'path' in config['pkmn_path']:
            destination_folder = os.path.join(config['pkmn_path']['path'], "graphics/object_events/pics/people/")
            
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            destination_path = os.path.join(destination_folder, os.path.basename(sprite_path))
            
            if os.path.abspath(sprite_path) != os.path.abspath(destination_path):
                shutil.copy(sprite_path, destination_path)

            if os.path.exists(destination_path):
                dpg.set_value("status_text", translator.get_text('sprite_moved'))
            else:
                dpg.set_value("status_text", translator.get_text('error_displaying_sprite_not_found'))
        else:
            dpg.set_value("status_text", translator.get_text('destination_folder_not_set'))
    else:
        dpg.set_value("status_text", translator.get_text('no_sprite_selected'))
