import dearpygui.dearpygui as dpg
import requests
import os

def verify_version(translator):
    url = "https://raw.githubusercontent.com/Nexxo11/AxoloteOwAdder/main/ver.txt"
    local_version_path = 'ver.txt'
    with open(local_version_path, 'r') as file:
        local_version = file.read().strip()
    response = requests.get(url)
    github_version = response.text.strip()
    if github_version > local_version:
        dpg.set_value("ver_status_text", translator.get_text('new_update_available'))
    else:
        dpg.set_value("ver_status_text", translator.get_text('have_latest_version'))
