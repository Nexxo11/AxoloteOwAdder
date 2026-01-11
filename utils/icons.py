import dearpygui.dearpygui as dpg
import os

TEXTURE_REGISTRY_TAG = "global_texture_registry"

def ensure_texture_registry():
    if not dpg.does_item_exist(TEXTURE_REGISTRY_TAG):
        with dpg.texture_registry(tag=TEXTURE_REGISTRY_TAG, show=False):
            pass

def register_icon(file_path, tag):
    """
    Loads an image from file_path and registers it as a static texture with the given tag.
    Returns True if successful, False otherwise.
    """
    if not os.path.exists(file_path):
        print(f"Icon file not found: {file_path}")
        return False
    
    if dpg.does_item_exist(tag):
        return True # Already registered

    try:
        width, height, channels, data = dpg.load_image(file_path)
        
        ensure_texture_registry()
        dpg.add_static_texture(width=width, height=height, default_value=data, tag=tag, parent=TEXTURE_REGISTRY_TAG)
        return True
    except Exception as e:
        print(f"Failed to load icon {file_path}: {e}")
        return False
