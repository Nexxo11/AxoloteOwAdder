import dearpygui.dearpygui as dpg

def setup_theme():
    with dpg.theme(tag="purple_theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 230, 255)) 
            dpg.add_theme_color(dpg.mvThemeCol_Border, (100, 70, 120))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (30, 30, 30))

        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (80, 80, 80))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (100, 100, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (120, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (120, 120, 180))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)

        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_Border, (80, 60, 120))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 230, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)

        with dpg.theme_component(dpg.mvInputInt):
            dpg.add_theme_color(dpg.mvThemeCol_Border, (80, 60, 120))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (70, 70, 100))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (90, 90, 130)) 
            dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 230, 255)) 
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5) 
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5) 
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 5) 

        with dpg.theme_component(dpg.mvCombo):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 50, 100))  
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (80, 80, 200))  
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5) 

        with dpg.theme_component(dpg.mvSliderInt):
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (120, 80, 180))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (150, 100, 200)) 

        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 60, 80)) 
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (80, 80, 120)) 
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (100, 100, 150)) 
            dpg.add_theme_color(dpg.mvThemeCol_Border, (50, 50, 80))  
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5) 
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5) 

    dpg.bind_theme("purple_theme")
