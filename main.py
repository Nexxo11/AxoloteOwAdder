import dearpygui.dearpygui as dpg
from ui.main_window import MainWindow
from translations.translator import Translator

if __name__ == "__main__":
    dpg.create_context()
    translator = Translator()
    main_window = MainWindow(translator)
    dpg.create_viewport(title='AxoloteOwAdder', width=540, height=660, resizable=False, small_icon='icon.ico')
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("primary_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
