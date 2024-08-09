import configparser
import tkinter as tk
from tkinter import filedialog
import dearpygui.dearpygui as dpg

config = configparser.ConfigParser()
config.read('path.ini')

def select_folder():
    root = tk.Tk()
    root.withdraw()  
    folder_selected = filedialog.askdirectory()

    if folder_selected:  
        
        if 'pkmn_ex_path' not in config:
            config['pkmn_ex_path'] = {}
        config['pkmn_ex_path']['path'] = folder_selected
        
        try:
            with open('path.ini', 'w') as configfile:
                config.write(configfile)
            dpg.set_value("folder_path_text", f"Selected Path: {folder_selected}")
        except PermissionError:
            print("Permission denied: 'path.ini'. Please check the file permissions or run the program as an administrator.")
        except Exception as e:
            print(f"An error occurred: {e}")

def insert_after_line_number(filename, line_number, insert_text):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    if line_number < len(lines):
        lines.insert(line_number + 1, insert_text + '\n')
    else:
        lines.append(insert_text + '\n')

    with open(filename, 'w') as f:
        f.writelines(lines)

def insert_line_in_structure(filename, structure_name, insert_text, insert_position=None):
    with open(filename, 'r') as f:
        lines = f.readlines()

    inside_structure = False
    structure_start_index = None
    indent_level = None

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        if stripped_line.startswith(structure_name):
            inside_structure = True
            structure_start_index = i
            indent_level = len(line) - len(line.lstrip()) + 4
            continue

        if inside_structure:
            current_indent = len(line) - len(line.lstrip())

            if stripped_line.startswith("};"):
                if insert_position is None:
                    lines.insert(i, " " * indent_level + insert_text + '\n')
                else:
                    lines.insert(structure_start_index + insert_position + 1, " " * indent_level + insert_text + '\n')
                break

    with open(filename, 'w') as f:
        f.writelines(lines)


def insert_overworld(overworld_name, overworld_id, palette_id, width, height, reflection_palette_tag, size, palette_slot, shadow_size, inanimate, tracks, frame_num):
    base_path = config['pkmn_ex_path']['path']

    defines_file = f"{base_path}/include/constants/event_objects.h"
    object_events_file = f"{base_path}/src/data/object_events/object_event_graphics.h"
    pic_tables_file = f"{base_path}/src/data/object_events/object_event_pic_tables.h"
    graphics_info_file = f"{base_path}/src/data/object_events/object_event_graphics_info.h"
    pointers_file = f"{base_path}/src/data/object_events/object_event_graphics_info_pointers.h"
    movement_file = f"{base_path}/src/event_object_movement.c"
    spritesheet_rules_file = f"{base_path}/spritesheet_rules.mk"

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
    insert_line_in_structure(pointers_file, 'const struct ObjectEventGraphicsInfo *const gObjectEventGraphicsInfoPointers[NUM_OBJ_EVENT_GFX]', f'[OBJ_EVENT_GFX_{overworld_name.upper()}] = &gObjectEventGraphicsInfo_{overworld_name},')
    insert_line_in_structure(movement_file, 'static const struct SpritePalette sObjectEventSpritePalettes[]', f'\t{{gObjectEventPal_{overworld_name}, OBJ_EVENT_PAL_TAG_{overworld_name.upper()}}},')

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

    with open('path.ini', 'w') as configfile:
        config.write(configfile)

    insert_overworld(overworld_name, overworld_id, palette_id, width, height, reflection_palette_tag, size, palette_slot, shadow_size, inanimate, tracks, frame_num)

    dpg.set_value("status_text", "The new overworld has been successfully inserted.")
