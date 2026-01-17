import dearpygui.dearpygui as dpg
import requests
import os
import re

def verify_version(translator):
    url = "https://raw.githubusercontent.com/Nexxo11/AxoloteOwAdder/main/ver.txt"
    local_version_path = 'ver.txt'
    with open(local_version_path, 'r', encoding='utf-8') as file:
        local_version = file.read().strip()
    response = requests.get(url)
    github_version = response.text.strip()
    if github_version > local_version:
        dpg.set_value("ver_status_text", translator.get_text('new_update_available'))
    else:
        dpg.set_value("ver_status_text", translator.get_text('have_latest_version'))

def check_project_compatibility(project_path, translator):
    """
    Checks the version of pokeemerald-expansion in README.md.
    Updates the UI text color: Green if >= 1.9.1, Red otherwise.
    """
    readme_path = os.path.join(project_path, "README.md")
    version = "Unknown"
    is_compatible = False
    
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Match: Based off RHH's pokeemerald-expansion 1.14.2 OR v1.8.0
                match = re.search(r"Based off RHH's pokeemerald-expansion\s+v?(\d+\.\d+\.\d+)", content)
                if match:
                    version = match.group(1)
                    # Simple tuple comparison
                    try:
                        v_parts = tuple(map(int, version.split('.')))
                        if v_parts >= (1, 9, 1):
                            is_compatible = True
                    except ValueError:
                        pass # Keep compatible as False if parsing fails
        except Exception as e:
            print(f"Error reading README.md: {e}")

    # UI Update
    if version == "Unknown":
        text = translator.get_text("compat_unknown")
        color = (255, 100, 100) # Red
    elif is_compatible:
        text = translator.get_text("compat_compatible").format(version=version)
        color = (100, 255, 100) # Green
    else:
        text = translator.get_text("compat_incompatible").format(version=version)
        color = (255, 100, 100) # Red

    if dpg.does_item_exist("expansion_ver_txt"):
        dpg.set_value("expansion_ver_txt", text)
        dpg.configure_item("expansion_ver_txt", color=color)
