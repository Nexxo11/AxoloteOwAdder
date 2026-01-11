import dearpygui.dearpygui as dpg
from ui.main_window import MainWindow
from translations.translator import Translator
import traceback

if __name__ == "__main__":
    try:
        dpg.create_context()
        translator = Translator()
        main_window = MainWindow(translator)
        dpg.create_viewport(title='AxoloteOwAdder',             width=600,
            height=720, resizable=False, small_icon='icon.ico')
        
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("primary_window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
    except Exception as e:
        with open("error.log", "w") as f:
            f.write(traceback.format_exc())
