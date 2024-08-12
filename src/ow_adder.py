import configparser
import tkinter as tk
from tkinter import filedialog
import dearpygui.dearpygui as dpg
import os
import shutil

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

def select_and_move_sprite():
    # Seleccionar el sprite
    root = tk.Tk()
    root.withdraw()
    sprite_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*")])

    if sprite_path:


        if dpg.does_item_exist("sprite_image"):
            dpg.delete_item("sprite_image")
        if dpg.does_item_exist("sprite_texture"):
            dpg.delete_item("sprite_texture")

        # Obtener la carpeta de destino
        config = configparser.ConfigParser()
        config.read('path.ini')
        
        if 'pkmn_ex_path' in config and 'path' in config['pkmn_ex_path']:
            destination_folder = os.path.join(config['pkmn_ex_path']['path'], "graphics/object_events/pics/people/")
            
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            # Mover el sprite a la carpeta destino
            destination_path = os.path.join(destination_folder, os.path.basename(sprite_path))
            shutil.move(sprite_path, destination_path)

            # Mostrar el sprite en la aplicación
            if os.path.exists(destination_path):
                try:
                    width, height, channels, data = dpg.load_image(destination_path)

                    # Obtener el tamaño del área de vista previa
                    preview_width = dpg.get_item_width("sprite_preview")
                    preview_height = dpg.get_item_height("sprite_preview")

                    # Calcular las coordenadas para centrar la imagen
                    pos_x = (preview_width - width) / 2 if width < preview_width else 0
                    pos_y = (preview_height - height) / 2 if height < preview_height else 0

                    # Si ya hay una imagen previa cargada, la eliminamos
                    if dpg.does_item_exist("sprite_image"):
                        dpg.delete_item("sprite_image")

                    # Crear una textura para la imagen
                    with dpg.texture_registry(show=False):
                        dpg.add_static_texture(width, height, data, tag="sprite_texture")

                    # Mostrar la imagen centrada en la ventana
                    dpg.add_image("sprite_texture", parent="sprite_preview", tag="sprite_image", pos=(pos_x, pos_y))
                    dpg.set_value("status_text", f"                             Sprite moved to\n             graphics/object_events/pics/people/ and displayed.")
                except Exception as e:
                    dpg.set_value("status_text", f"Error displaying sprite: {str(e)}")
            else:
                dpg.set_value("status_text", "                           Error displaying sprite. File not found.")
        else:
            dpg.set_value("status_text", "                       Destination folder not set. \n           Please select the pokeemerald-expansion folder first.")
    else:
        dpg.set_value("status_text", "                           No sprite selected.")

def get_next_define_number(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    last_define = None
    for line in lines:
        line = line.strip()
        if line.startswith("#define"):
            parts = line.split()
            if len(parts) == 3 and parts[1].startswith('OBJ_EVENT_GFX'):
                try:
                    number = int(parts[2])
                    if last_define is None or number > last_define:
                        last_define = number
                except ValueError:
                    pass
    
    if last_define is not None:
        return last_define + 1
    else:
        return 1

def get_next_hex_define_number(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    last_define = None
    for line in lines:
        line = line.strip()
        if line.startswith("#define"):
            parts = line.split()
            if len(parts) == 3 and parts[1].startswith('OBJ_EVENT_PAL_TAG'):
                try:
                    number = int(parts[2], 16)
                    if last_define is None or number > last_define:
                        last_define = number
                except ValueError:
                    pass
    
    if last_define is not None:
        return last_define + 1
    else:
        return 0x111E


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


def insert_overworld(overworld_name, width, height, reflection_palette_tag, size, palette_slot, shadow_size, inanimate, tracks, frame_num, anim_table):
    base_path = config['pkmn_ex_path']['path']

    defines_file = f"{base_path}/include/constants/event_objects.h"
    object_events_file = f"{base_path}/src/data/object_events/object_event_graphics.h"
    pic_tables_file = f"{base_path}/src/data/object_events/object_event_pic_tables.h"
    graphics_info_file = f"{base_path}/src/data/object_events/object_event_graphics_info.h"
    pointers_file = f"{base_path}/src/data/object_events/object_event_graphics_info_pointers.h"
    movement_file = f"{base_path}/src/event_object_movement.c"
    spritesheet_rules_file = f"{base_path}/spritesheet_rules.mk"

    next_define_id = get_next_define_number(defines_file)
    next_define_hex_id = get_next_hex_define_number(defines_file)

    global define_overworld_id
    global define_overworld_hex_id
    define_overworld_id = next_define_id
    define_overworld_hex_id = next_define_hex_id

    with open(defines_file, 'a') as f:
        f.write(f'#define OBJ_EVENT_GFX_{overworld_name.upper()} {next_define_id}\n')
        f.write(f"#define OBJ_EVENT_PAL_TAG_{overworld_name.upper()} 0x{next_define_hex_id:04X}\n")

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
    .anims = sAnimTable_{anim_table},
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
    #overworld_id = int(dpg.get_value("overworld_id"))
    #palette_id = int(dpg.get_value("palette_id"), 16)
    width = int(dpg.get_value("width"))
    height = int(dpg.get_value("height"))
    frame_num = int(dpg.get_value("frame_num"))
    reflection_palette_tag = dpg.get_value("reflection_palette_tag")
    size = int(width * height / 2)
    palette_slot = dpg.get_value("palette_slot")
    shadow_size = dpg.get_value("shadow_size")
    inanimate = dpg.get_value("inanimate")
    tracks = dpg.get_value("tracks")
    anim_table = dpg.get_value("anim_table")

    with open('path.ini', 'w') as configfile:
        config.write(configfile)
    if overworld_name.strip():
        try:
            if (width == 16 and height == 64) or (width == 64 and height == 16):
                dpg.set_value("status_text", "Invalid width and height combination (16x64 or 64x16 not allowed).")
            else:
                insert_overworld(
                    overworld_name, width, height, 
                    reflection_palette_tag, size, palette_slot, shadow_size, 
                    inanimate, tracks, frame_num, anim_table
                )
                dpg.set_value("status_text", f"            The new overworld has been successfully inserted.\n                            GfxID: {define_overworld_id}  PalID: 0x{define_overworld_hex_id:04X}")
        except Exception as e:
            dpg.set_value("status_text", f"            Error inserting overworld: {e}")
    else:
        dpg.set_value("status_text", "                       Overworld Name Not Provided")