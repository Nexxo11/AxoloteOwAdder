import dearpygui.dearpygui as dpg
import configparser
import tkinter as tk
from tkinter import filedialog

config = configparser.ConfigParser()
config.read('path.ini')

def select_folder():
    root = tk.Tk()
    root.withdraw()  
    folder_selected = filedialog.askdirectory()

    if folder_selected:  
        info_pointers_index = 491
        
        if 'pkmn_ex_path' not in config:
            config['pkmn_ex_path'] = {}
        config['pkmn_ex_path']['path'] = folder_selected
        config['pkmn_ex_path']['info_pointers_index'] = str(info_pointers_index)
        
        try:
            with open('path.ini', 'w') as configfile:
                config.write(configfile)
            dpg.set_value("folder_path_text", f"Selected Path: {folder_selected}")
        except PermissionError:
            print("Permission denied: 'path.ini'. Please check the file permissions or run the program as an administrator.")
        except Exception as e:
            print(f"An error occurred: {e}")

def insert_after_line(filename, search_text, insert_text):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if search_text in line:
            lines.insert(i + 1, insert_text)
            break

    with open(filename, 'w') as f:
        f.writelines(lines)

def insert_after_line_number(filename, line_number, insert_text):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    if line_number < len(lines):
        lines.insert(line_number + 1, insert_text + '\n')
    else:
        lines.append(insert_text + '\n')

    with open(filename, 'w') as f:
        f.writelines(lines)

def insert_overworld(overworld_name, overworld_id, palette_id, width, height, reflection_palette_tag, size, palette_slot, shadow_size, inanimate, tracks, frame_num, info_pointers_index):
    base_path = config['pkmn_ex_path']['path']

    # Files to modify
    defines_file = f"{base_path}/include/constants/event_objects.h"
    object_events_file = f"{base_path}/src/data/object_events/object_event_graphics.h"
    pic_tables_file = f"{base_path}/src/data/object_events/object_event_pic_tables.h"
    graphics_info_file = f"{base_path}/src/data/object_events/object_event_graphics_info.h"
    pointers_file = f"{base_path}/src/data/object_events/object_event_graphics_info_pointers.h"
    movement_file = f"{base_path}/src/event_object_movement.c"
    spritesheet_rules_file = f"{base_path}/spritesheet_rules.mk"

    #insert_after_line_number(defines_file, 244, f'#define OBJ_EVENT_GFX_{overworld_name.upper()} {overworld_id}')
    #insert_after_line_number(defines_file, event_object_pal, f'#define OBJ_EVENT_PAL_TAG_{overworld_name.upper()} {hex(palette_id)}')
    with open(defines_file, 'a') as f:
        f.write(f'#define OBJ_EVENT_GFX_{overworld_name.upper()} {overworld_id}\n')
        f.write(f"#define OBJ_EVENT_PAL_TAG_{overworld_name.upper()} {hex(palette_id)}\n")

    with open(object_events_file, 'a') as f:
        f.write(f'const u16 gObjectEventPal_{overworld_name}[] = INCBIN_U16("graphics/object_events/pics/people/{overworld_name}.gbapal");\n')
        f.write(f'const u32 gObjectEventPic_{overworld_name}[] = INCBIN_U32("graphics/object_events/pics/people/{overworld_name}.4bpp");\n')

    frames = "\n".join([f'    overworld_frame(gObjectEventPic_{overworld_name}, {width//8}, {height//8}, {i}),' for i in range(frame_num)])
    with open(pic_tables_file, 'a') as f:
        f.write(f'\nstatic const struct SpriteFrameImage sPicTable_{overworld_name}[] = {{\n{frames}\n}};\n')

    with open(graphics_info_file, 'a') as f:
        f.write(f"""
const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{overworld_name} = {{
    .tileTag = TAG_NONE,
    .paletteTag = OBJ_EVENT_PAL_TAG_{overworld_name.upper()},
    .reflectionPaletteTag = {reflection_palette_tag},
    .size = {size},
    .width = {width},
    .height = {height},
    .paletteSlot = {palette_slot},
    .shadowSize = {shadow_size},
    .inanimate = {inanimate},
    .compressed = FALSE,
    .tracks = {tracks},
    .oam = &gObjectEventBaseOam_{width}x{height},
    .subspriteTables = sOamTables_{width}x{height},
    .anims = sAnimTable_Standard,
    .images = sPicTable_{overworld_name},
    .affineAnims = gDummySpriteAffineAnimTable,
}};
""")

    insert_after_line_number(pointers_file, 0, f'extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{overworld_name};')
    insert_after_line_number(pointers_file, info_pointers_index, f'\t[OBJ_EVENT_GFX_{overworld_name.upper()}] = &gObjectEventGraphicsInfo_{overworld_name},')
    insert_after_line_number(movement_file, 473, f'\t{{gObjectEventPal_{overworld_name}, OBJ_EVENT_PAL_TAG_{overworld_name.upper()}}},')

    with open(spritesheet_rules_file, 'a') as f:
        f.write(f'\n$(OBJEVENTGFXDIR)/people/{overworld_name}.4bpp: %.4bpp: %.png\n')
        f.write(f'\t$(GFX) $< $@ -mwidth {width//8} -mheight {height//8}\n')

def insert_overworld_gui():
    overworld_name = dpg.get_value("overworld_name")
    overworld_id = int(dpg.get_value("overworld_id"))
    palette_id = int(dpg.get_value("palette_id"), 16)
    width = int(dpg.get_value("width"))
    height = int(dpg.get_value("height"))
    frame_num = int(dpg.get_value("frame_num"))
    reflection_palette_tag = dpg.get_value("reflection_palette_tag")
    size = int(width * height / 2)
    palette_slot = dpg.get_value("palette_slot")
    shadow_size = dpg.get_value("shadow_size")
    inanimate = dpg.get_value("inanimate")
    tracks = dpg.get_value("tracks")

    info_pointers_index = int(config['pkmn_ex_path']['info_pointers_index']) + 1
    config['pkmn_ex_path']['info_pointers_index'] = str(info_pointers_index)
    with open('path.ini', 'w') as configfile:
        config.write(configfile)

    insert_overworld(overworld_name, overworld_id, palette_id, width, height, reflection_palette_tag, size, palette_slot, shadow_size, inanimate, tracks, frame_num, info_pointers_index)

    dpg.set_value("status_text", "The new overworld has been successfully inserted.")

dpg.create_context()

with dpg.window(tag="primary_window", label="Insert Overworld", width=600, height=400):
    dpg.add_text("Insert Overworld Parameters")
    
    dpg.add_button(label="Select pokeemerald-expansion Folder", callback=select_folder)
    dpg.add_text("If you have a path file config, you don't need to load it again", tag="folder_path_text")
    
    dpg.add_input_text(label="Overworld Name", tag="overworld_name")     
    dpg.add_input_text(label="Overworld ID", tag="overworld_id", default_value="241")
    dpg.add_input_text(label="Palette ID (hex)", tag="palette_id", default_value="1125")
    
    dpg.add_combo(label="Width", items=["16", "32", "64"], tag="width", default_value="32")
    dpg.add_combo(label="Height", items=["16", "32", "64"], tag="height", default_value="32")

    dpg.add_input_int(label="Frame Number", tag="frame_num", default_value=9)
    dpg.add_input_text(label="Reflection Palette Tag", tag="reflection_palette_tag", default_value="OBJ_EVENT_PAL_TAG_NONE")
    dpg.add_combo(label="Palette Slot", items=["PALSLOT_PLAYER", "PALSLOT_NPC_1", "PALSLOT_NPC_2", "PALSLOT_NPC_3", "PALSLOT_NPC_4", "PALSLOT_NPC_5", "PALSLOT_NPC_6", "PALSLOT_NPC_7"], tag="palette_slot", default_value="PALSLOT_NPC_1")
    dpg.add_combo(label="Shadow Size", items=["SHADOW_SIZE_S", "SHADOW_SIZE_M", "SHADOW_SIZE_L", "SHADOW_SIZE_XL"], tag="shadow_size", default_value="SHADOW_SIZE_M")
    dpg.add_combo(label="Inanimate", items=["TRUE", "FALSE"], tag="inanimate", default_value="FALSE")
    dpg.add_combo(label="Tracks", items=["TRUE", "FALSE"], tag="tracks", default_value="FALSE")

    dpg.add_button(label="Insert Overworld", callback=insert_overworld_gui)
    dpg.add_text("", tag="status_text")

    dpg.add_text("By Nexxo", pos=(500, 25))
    dpg.add_text("Compatible expansion version: 1.9.0")

dpg.create_viewport(title='AxoloteOwAdder', width=620, height=460, resizable=False)
dpg.set_primary_window("primary_window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
