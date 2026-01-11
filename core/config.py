import configparser
import tkinter as tk
from tkinter import filedialog
import dearpygui.dearpygui as dpg
from core.version import check_project_compatibility

config = configparser.ConfigParser()
config.read('path.ini')

def select_folder(translator):
    root = tk.Tk()
    root.withdraw()  
    folder_selected = filedialog.askdirectory()

    if folder_selected:  
        
        if 'pkmn_path' not in config:
            config['pkmn_path'] = {}
        config['pkmn_path']['path'] = folder_selected
        
        try:
            with open('path.ini', 'w') as configfile:
                config.write(configfile)
            dpg.set_value("folder_path_text", f"{translator.get_text('selected_path')}{folder_selected}")
            
            # Check compatibility
            check_project_compatibility(folder_selected, translator)
            
            dpg.configure_item("popup_window", show=True)
        except PermissionError:
            print(translator.get_text('permission_denied'))
            dpg.configure_item("popup_window", show=True)
        except Exception as e:
            print(f"{translator.get_text('error_occurred')}{e}")

def complete_config(translator):
    selected_project = dpg.get_value("project_setting_ver")
    dynamic_pal = dpg.get_value("project_setting_pal")
    with open('path.ini', 'w') as configfile:
        config['pkmn_path']['project_version'] = selected_project
        config['pkmn_path']['dynamic_pal_system'] = str(dynamic_pal)
        config.write(configfile)
    
    dpg.configure_item("popup_window", show=False)
