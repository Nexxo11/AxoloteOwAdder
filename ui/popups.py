import dearpygui.dearpygui as dpg
from core.config import complete_config

def _perform_delete():
    """Imports and calls the core deletion logic to avoid circular imports at startup."""
    from core.adder import delete_overworld
    
    user_data = dpg.get_item_user_data("delete_confirmation_popup")
    overworld_name = user_data["name"]
    translator = user_data["translator"]
    callback = user_data.get("callback")
    
    dpg.configure_item("delete_confirmation_popup", show=False)
    delete_overworld(overworld_name, translator)
    
    if callback:
        callback()

def show_delete_confirmation(translator, callback=None):
    """Gets the overworld name from the input and shows the delete confirmation modal."""
    overworld_name = dpg.get_value("overworld_name")
    if not overworld_name.strip():
        dpg.set_value("status_text", translator.get_text('overworld_name_not_provided'))
        return

    confirm_text = translator.get_text('delete_confirm_text').format(name=overworld_name)
    dpg.set_value("delete_confirm_text_id", confirm_text)
    dpg.set_item_user_data("delete_confirmation_popup", {
        "name": overworld_name, 
        "translator": translator,
        "callback": callback
    })
    dpg.configure_item("delete_confirmation_popup", show=True)

def setup_popups(translator):
    """Sets up all modal windows for the application."""
    # Original project configuration popup
    with dpg.window(tag="popup_window", label="Configure Project", modal=True, show=False, no_resize=True, no_close=True):
        dpg.add_text("Select the option that matches your project")
        dpg.add_combo(items=["Pokeemerald", "Poke-expansion"], tag="project_setting_ver", default_value="Poke-expansion")
        dpg.add_separator()
        dpg.add_checkbox(label="Dynamic Pal System", tag="project_setting_pal", default_value=True)
        dpg.add_separator()
        dpg.add_button(label="Complete", callback=lambda: complete_config(translator))

    # New delete confirmation popup
    with dpg.window(tag="delete_confirmation_popup", label="Confirm Deletion", modal=True, show=False, no_resize=True):
        dpg.add_text("Are you sure?", tag="delete_confirm_text_id")
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_button(label="Yes", callback=_perform_delete, width=75)
            dpg.add_button(label="No", callback=lambda: dpg.configure_item("delete_confirmation_popup", show=False), width=75)