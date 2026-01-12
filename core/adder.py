import configparser
import shutil
import os
import dearpygui.dearpygui as dpg
from core import defines
from utils.file_system import insert_after_line_number, insert_line_in_structure

config = configparser.ConfigParser()
config.read('path.ini')

def create_backups(file_paths):
    """Creates a backup (.bak) of the specified files."""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                shutil.copy(file_path, f"{file_path}.bak")
        except Exception as e:
            print(f"Warning: Could not create backup for {file_path}: {e}")

def restore_backups(translator):
    """Restores files from their .bak backups if they exist."""
    config.read('path.ini')
    if not config.has_section('pkmn_path') or 'path' not in config['pkmn_path']:
        dpg.set_value("status_text", translator.get_text('destination_folder_not_set'))
        return

    base_path = config['pkmn_path']['path']
    if not base_path:
        dpg.set_value("status_text", translator.get_text('destination_folder_not_set'))
        return

    files_to_restore = [
        f"{base_path}/include/constants/event_objects.h",
        f"{base_path}/src/data/object_events/object_event_graphics.h",
        f"{base_path}/src/data/object_events/object_event_pic_tables.h",
        f"{base_path}/src/data/object_events/object_event_graphics_info.h",
        f"{base_path}/src/data/object_events/object_event_graphics_info_pointers.h",
        f"{base_path}/src/event_object_movement.c",
        f"{base_path}/spritesheet_rules.mk"
    ]

    restored_count = 0
    for file_path in files_to_restore:
        backup_path = f"{file_path}.bak"
        try:
            if os.path.exists(backup_path):
                shutil.copy(backup_path, file_path)
                os.remove(backup_path)
                restored_count += 1
        except Exception as e:
            print(f"Error restoring {file_path}: {e}")

    if restored_count > 0:
        dpg.set_value("status_text", translator.get_text('restore_success').format(count=restored_count))
    else:
        dpg.set_value("status_text", translator.get_text('restore_no_backups'))

def write_graphics_info(file, overworld_name, pal_tag, reflection_palette_tag, size, width, height, palette_slot, shadow_size, inanimate, tracks, anim_table, extra_field):
    file.write(f"""
const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{overworld_name} =
{{
    .tileTag = TAG_NONE,
    .paletteTag = {pal_tag},
    .reflectionPaletteTag = {reflection_palette_tag},
    .size = {size},
    .width = {width},
    .height = {height},
    .paletteSlot = {palette_slot},
    .shadowSize = {shadow_size},
    .inanimate = {inanimate},
    {extra_field}
    .tracks = {tracks},
    .oam = &gObjectEventBaseOam_{width}x{height},
    .subspriteTables = sOamTables_{width}x{height},
    .anims = sAnimTable_{anim_table},
    .images = sPicTable_{overworld_name},
    .affineAnims = gDummySpriteAffineAnimTable,
}};
""")

def insert_overworld(overworld_name, width, height, reflection_palette_tag, size, palette_slot, shadow_size, inanimate, tracks, frame_num, anim_table, pal_tag, disableReflection):
    base_path = config['pkmn_path']['path']

    defines_file = f"{base_path}/include/constants/event_objects.h"
    object_events_file = f"{base_path}/src/data/object_events/object_event_graphics.h"
    pic_tables_file = f"{base_path}/src/data/object_events/object_event_pic_tables.h"
    graphics_info_file = f"{base_path}/src/data/object_events/object_event_graphics_info.h"
    pointers_file = f"{base_path}/src/data/object_events/object_event_graphics_info_pointers.h"
    movement_file = f"{base_path}/src/event_object_movement.c"
    spritesheet_rules_file = f"{base_path}/spritesheet_rules.mk"

    # Create backups before modification
    create_backups([
        defines_file, object_events_file, pic_tables_file, 
        graphics_info_file, pointers_file, movement_file, spritesheet_rules_file
    ])

    next_define_id = defines.get_next_define_number(defines_file)
    next_define_hex_id = defines.get_next_pal_tag_define_number(defines_file)

    global define_overworld_id
    global define_overworld_hex_id
    define_overworld_id = next_define_id
    define_overworld_hex_id = next_define_hex_id

    if 'pkmn_path' in config:
        if 'project_version' in config['pkmn_path']:
            project_version = config['pkmn_path']['project_version']
            dynamic_pal_system = config['pkmn_path']['dynamic_pal_system']
        else:
            # Default to Poke-expansion if not specified
            project_version = 'Poke-expansion'
            dynamic_pal_system = 'True'
    else:
        project_version = 'Poke-expansion'
        dynamic_pal_system = 'True'

    with open(defines_file, 'r') as f:
        lines = f.readlines()

    endif_index = -1
    # Search for the specific guard first
    for i, line in enumerate(lines):
        if line.strip().startswith("#endif") and "GUARD_CONSTANTS_EVENT_OBJECTS_H" in line:
            endif_index = i
            break
    
    # Fallback: Find the last #endif if the guard isn't explicit
    if endif_index == -1:
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith("#endif"):
                endif_index = i
                break

    if endif_index != -1:
        if project_version == 'Poke-expansion':
            lines.insert(endif_index, f'#define OBJ_EVENT_GFX_{overworld_name.upper()} {next_define_id}\n')
            lines.insert(endif_index + 1, f'#define OBJ_EVENT_PAL_TAG_{overworld_name.upper()} 0x{next_define_hex_id:04X}\n')
        elif project_version == 'Pokeemerald' and dynamic_pal_system == 'True':
            lines.insert(endif_index, f'#define OBJ_EVENT_GFX_{overworld_name.upper()} {next_define_id}\n')
            lines.insert(endif_index + 1, f'#define OBJ_EVENT_PAL_TAG_{overworld_name.upper()} 0x{next_define_hex_id:04X}\n')
            defines.define_pal_emerald_hex_id = next_define_hex_id
        elif project_version == 'Pokeemerald' and dynamic_pal_system == 'False':
            lines.insert(endif_index, f'#define OBJ_EVENT_GFX_{overworld_name.upper()} {next_define_id}\n')

    with open(defines_file, 'w') as f:
        f.writelines(lines)

    with open(object_events_file, 'a') as f:
        f.write(f'const u32 gObjectEventPic_{overworld_name}[] = INCBIN_U32("graphics/object_events/pics/people/{overworld_name}.4bpp");\n')
        if dynamic_pal_system == 'True' or project_version == 'Poke-expansion':
            f.write(f'const u16 gObjectEventPal_{overworld_name}[] = INCBIN_U16("graphics/object_events/pics/people/{overworld_name}.gbapal");\n')

    frames = "\n".join([f'    overworld_frame(gObjectEventPic_{overworld_name}, {width//8}, {height//8}, {i}),' for i in range(frame_num)])
    with open(pic_tables_file, 'a') as f:
                f.write(f'\nstatic const struct SpriteFrameImage sPicTable_{overworld_name}[] = {{{frames}}};')

    with open(graphics_info_file, 'a') as f:
        if project_version == 'Poke-expansion':
            write_graphics_info(
                f, overworld_name, f'OBJ_EVENT_PAL_TAG_{overworld_name.upper()}', reflection_palette_tag,
                size, width, height, palette_slot, shadow_size, inanimate, tracks, anim_table, '.compressed = FALSE,'
            )
        elif project_version == 'Pokeemerald':
            if dynamic_pal_system == 'True':
                pal_tag = f'OBJ_EVENT_PAL_TAG_{overworld_name.upper()}'
            else:
                pal_tag = f'OBJ_EVENT_PAL_TAG_{pal_tag.upper()}'
            
            # Only explicitly write if TRUE. If FALSE, omitting it defaults to 0 (False) in Pokeemerald,
            # and prevents "no member named..." error in Poke-expansion.
            extra_field = f'.disableReflectionPaletteLoad = {disableReflection},' if disableReflection == 'TRUE' else ''
            
            write_graphics_info(
                f, overworld_name, pal_tag, reflection_palette_tag, size, width, height, palette_slot,
                shadow_size, inanimate, tracks, anim_table, extra_field
            )


    insert_after_line_number(pointers_file, 0, f'extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{overworld_name};')
    insert_line_in_structure(pointers_file, 'const struct ObjectEventGraphicsInfo *const gObjectEventGraphicsInfoPointers[NUM_OBJ_EVENT_GFX]', f'[OBJ_EVENT_GFX_{overworld_name.upper()}] = &gObjectEventGraphicsInfo_{overworld_name},')
    if dynamic_pal_system == 'True' or project_version == 'Poke-expansion':
        insert_line_in_structure(movement_file, 'static const struct SpritePalette sObjectEventSpritePalettes[]', f'\t{{gObjectEventPal_{overworld_name}, OBJ_EVENT_PAL_TAG_{overworld_name.upper()}}},', insert_position=0)
    #else:
    #    insert_line_in_structure(movement_file, 'static const struct SpritePalette sObjectEventSpritePalettes[]', f'\t{{gObjectEventPal_{pal_tag.capitalize()}, OBJ_EVENT_PAL_TAG_{pal_tag.upper()}}},')

    with open(spritesheet_rules_file, 'a') as f:
        f.write(f'\n$(OBJEVENTGFXDIR)/people/{overworld_name}.4bpp: %.4bpp: %.png\n')
        f.write(f'\t$(GFX) $< $@ -mwidth {width//8} -mheight {height//8}\n')

def overworld_exists(overworld_name):
    config.read('path.ini')
    base_path = config['pkmn_path']['path']
    defines_file = f"{base_path}/include/constants/event_objects.h"
    search_string = f"#define OBJ_EVENT_GFX_{overworld_name.upper()}"
    try:
        with open(defines_file, 'r', encoding='utf-8') as f:
            if search_string in f.read():
                return True
    except FileNotFoundError:
        return False
    return False

def get_custom_overworlds():
    """Scans the event_objects.h file to find overworld definitions."""
    config.read('path.ini')
    overworlds = []
    base_path = config['pkmn_path'].get('path', '')
    if not base_path:
        return []
        
    defines_file = f"{base_path}/include/constants/event_objects.h"
    
    try:
        with open(defines_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            # Look for #define OBJ_EVENT_GFX_NAME Value
            if line.startswith("#define OBJ_EVENT_GFX_"):
                parts = line.split()
                if len(parts) >= 2:
                    define_name = parts[1]
                    # Extract NAME from OBJ_EVENT_GFX_NAME
                    name = define_name.replace("OBJ_EVENT_GFX_", "").lower()
                    # Filter out standard system defines if necessary, 
                    # but usually custom ones are appended.
                    # Simple heuristic: Only return those that likely match user input format
                    overworlds.append(name)
                    
    except FileNotFoundError:
        pass
        
    return sorted(overworlds)

def insert_overworld_gui(translator):
    config.read('path.ini')
    overworld_name = dpg.get_value("overworld_name")

    if not overworld_name.strip():
        dpg.set_value("status_text", translator.get_text('overworld_name_not_provided'))
        return

    if overworld_exists(overworld_name):
        dpg.set_value("status_text", translator.get_text('overworld_already_exists').format(name=overworld_name))
        return

    try:
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
        pal_tag = dpg.get_value("pal_tag")
        disableReflection = dpg.get_value("disableReflection")

        if 'pkmn_path' in config:
            if 'dynamic_pal_system' in config['pkmn_path']:
                dynamic_pal_system = config['pkmn_path']['dynamic_pal_system']
                project_version = config['pkmn_path']['project_version']

        with open('path.ini', 'w') as configfile:
            config.write(configfile)

        if (width == 16 and height == 64) or (width == 64 and height == 16):
            dpg.set_value("status_text", translator.get_text('invalid_width_height'))
        else:
            insert_overworld(
                overworld_name, width, height,
                reflection_palette_tag, size, palette_slot, shadow_size,
                inanimate, tracks, frame_num, anim_table, pal_tag, disableReflection
            )
            new_value = defines.update_num_obj_event_gfx()
            success_msg = translator.get_text('overworld_inserted')
            update_msg = f"{translator.get_text('num_obj_event_gfx_updated')} {new_value}"

            if project_version == 'Poke-expansion':
                info_msg = f"GfxID: {define_overworld_id}\nPalID: 0x{define_overworld_hex_id:04X}"
                dpg.set_value("status_text", f"{success_msg}\n{info_msg}\n{update_msg}")
            elif project_version == 'Pokeemerald' and dynamic_pal_system == 'True':
                info_msg = f"GfxID: {define_overworld_id}\nPalID: 0x{defines.define_pal_emerald_hex_id:04X}"
                dpg.set_value("status_text", f"{success_msg}\n{info_msg}\n{update_msg}")
            else:
                info_msg = f"GfxID: {define_overworld_id}\nPalette: OBJ_EVENT_PAL_TAG_{pal_tag}"
                dpg.set_value("status_text", f"{success_msg}\n{info_msg}\n{update_msg}")
    except Exception as e:
        dpg.set_value("status_text", f"{translator.get_text('error_inserting_overworld')}{e}")

def _remove_lines_from_file(file_path, strings_to_find):
    """Helper function to remove lines containing any of the given strings."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        original_line_count = len(lines)
        lines = [line for line in lines if not any(s in line for s in strings_to_find)]
        
        if len(lines) < original_line_count:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
    except FileNotFoundError:
        pass

def _remove_block_from_file(file_path, start_str, end_str="}};"):
    """Helper function to remove a block of code and any preceding blank line."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        in_block = False
        found = False
        skip_next_empty = False
        for line in lines:
            if skip_next_empty:
                skip_next_empty = False
                if line.strip() == "":
                    continue
            if not in_block and start_str in line:
                in_block = True
                found = True
                # If the last line added was just a blank line, pop it to remove the empty space.
                if new_lines and new_lines[-1].strip() == "":
                    new_lines.pop()
                continue
            if in_block and end_str in line:
                in_block = False
                skip_next_empty = True
                continue
            if not in_block:
                new_lines.append(line)
        
        if found:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
    except FileNotFoundError:
        pass

import re

def find_default_overworld(base_path, exclude_name):
    """
    Finds a valid default overworld define from event_objects.h.
    Prefer 'OBJ_EVENT_GFX_LITTLE_BOY' or 'OBJ_EVENT_GFX_BOY_1'.
    """
    defines_file = os.path.join(base_path, "include", "constants", "event_objects.h")
    candidates = ["OBJ_EVENT_GFX_LITTLE_BOY", "OBJ_EVENT_GFX_BOY_1", "OBJ_EVENT_GFX_VAR_0"]
    
    try:
        with open(defines_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for cand in candidates:
            if f"#define {cand}" in content:
                return cand
        
        # If preferred not found, grab the first valid OBJ_EVENT_GFX_ define
        matches = re.findall(r'#define (OBJ_EVENT_GFX_\w+)', content)
        exclude_define = f"OBJ_EVENT_GFX_{exclude_name.upper()}"
        for match in matches:
            if match != exclude_define:
                return match
                
    except Exception as e:
        print(f"Warning: Could not find default overworld: {e}")
    
    return "OBJ_EVENT_GFX_VAR_0" # Ultimate fallback

def replace_map_references(base_path, deleted_name, replacement_define):
    """
    Scans data/maps for map.json and events.inc and replaces the deleted overworld define.
    """
    maps_dir = os.path.join(base_path, "data", "maps")
    target_define = f"OBJ_EVENT_GFX_{deleted_name.upper()}"
    
    if not os.path.exists(maps_dir):
        return 0

    count = 0
    # Walk through all map directories
    for root, dirs, files in os.walk(maps_dir):
        for file in files:
            if file in ["map.json", "events.inc"]:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if target_define in content:
                        # Replace word boundary to ensure exact match
                        # Using simple string replace might be safer if boundaries are known, 
                        # but regex is better to avoid partial matches (e.g. OBJ_EVENT_GFX_NAME_TWO)
                        # However, for map.json/inc, boundaries are usually quotes or commas.
                        # Let's use regex for safety.
                        pattern = r'\b' + re.escape(target_define) + r'\b'
                        if re.search(pattern, content):
                            new_content = re.sub(pattern, replacement_define, content)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            count += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    return count

def _get_cased_overworld_name(base_path, overworld_name):
    """
    Attempts to find the exact casing of the overworld name as used in
    object_event_graphics.h (e.g. gObjectEventPic_Name).
    Returns the found name (with case) or the original if not found.
    """
    object_events_file = f"{base_path}/src/data/object_events/object_event_graphics.h"
    try:
        with open(object_events_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        lower_name = overworld_name.lower()
        search_prefix = "const u32 gObjectEventPic_"
        
        for line in lines:
            if search_prefix in line:
                # expected line: const u32 gObjectEventPic_Name[] = ...
                # Extract "Name"
                parts = line.split(search_prefix)
                if len(parts) > 1:
                    # content after prefix: Name[] = ...
                    rest = parts[1]
                    if "[]" in rest:
                        found_name = rest.split("[]")[0]
                        if found_name.lower() == lower_name:
                            return found_name
    except FileNotFoundError:
        pass
    
    return overworld_name

def delete_overworld(overworld_name, translator):
    """Main function to delete an overworld and all its references."""
    try:
        if not overworld_exists(overworld_name):
            dpg.set_value("status_text", translator.get_text('delete_not_found').format(name=overworld_name))
            return

        base_path = config['pkmn_path']['path']
        
        # Replace references in maps
        default_ow = find_default_overworld(base_path, overworld_name)
        replaced_count = replace_map_references(base_path, overworld_name, default_ow)

        # Resolve the correct casing used in the C files
        cased_overworld_name = _get_cased_overworld_name(base_path, overworld_name)
        
        # Use cased_overworld_name for code references, 
        # but KEEP uppercase for defines (as they are always UPPER).
        
        project_version = config['pkmn_path'].get('project_version', 'Pokeemerald')
        dynamic_pal_system = config['pkmn_path'].get('dynamic_pal_system', 'False')

        defines_file = f"{base_path}/include/constants/event_objects.h"
        object_events_file = f"{base_path}/src/data/object_events/object_event_graphics.h"
        pic_tables_file = f"{base_path}/src/data/object_events/object_event_pic_tables.h"
        graphics_info_file = f"{base_path}/src/data/object_events/object_event_graphics_info.h"
        pointers_file = f"{base_path}/src/data/object_events/object_event_graphics_info_pointers.h"
        movement_file = f"{base_path}/src/event_object_movement.c"
        spritesheet_rules_file = f"{base_path}/spritesheet_rules.mk"

        # Image files to delete
        image_files = [
            f"{base_path}/graphics/object_events/pics/people/{cased_overworld_name}.png",
            f"{base_path}/graphics/object_events/pics/people/{cased_overworld_name}.4bpp",
            f"{base_path}/graphics/object_events/pics/people/{cased_overworld_name}.gbapal"
        ]

        # Create backups before modification
        create_backups([
            defines_file, object_events_file, pic_tables_file, 
            graphics_info_file, pointers_file, movement_file, spritesheet_rules_file
        ])

        defines_to_remove = [
            f"OBJ_EVENT_GFX_{overworld_name.upper()}",
            f"OBJ_EVENT_PAL_TAG_{overworld_name.upper()}"
        ]
        _remove_lines_from_file(defines_file, defines_to_remove)

        incbins_to_remove = [f"gObjectEventPic_{cased_overworld_name}[]", f"gObjectEventPal_{cased_overworld_name}[]"]
        _remove_lines_from_file(object_events_file, incbins_to_remove)

        _remove_block_from_file(pic_tables_file, f"sPicTable_{cased_overworld_name}[]", end_str="};")
        _remove_block_from_file(graphics_info_file, f"gObjectEventGraphicsInfo_{cased_overworld_name}", end_str="};")

        pointers_to_remove = [
            f"gObjectEventGraphicsInfo_{cased_overworld_name}",
            f"[OBJ_EVENT_GFX_{overworld_name.upper()}]"
        ]
        _remove_lines_from_file(pointers_file, pointers_to_remove)

        _remove_lines_from_file(movement_file, [f"gObjectEventPal_{cased_overworld_name}"])

        with open(spritesheet_rules_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        new_lines = []
        skip_next = False
        target_rule = f"/{overworld_name}.4bpp:".lower()
        for line in lines:
            if skip_next:
                skip_next = False
                continue
            if target_rule in line.lower():
                skip_next = True
                if new_lines and new_lines[-1].strip() == "":
                    new_lines.pop()
                continue
            new_lines.append(line)
        with open(spritesheet_rules_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        defines.update_num_obj_event_gfx(increment=False)

        # Remove image files
        for img_file in image_files:
            if os.path.exists(img_file):
                try:
                    os.remove(img_file)
                except Exception as e:
                    print(f"Warning: Could not remove {img_file}: {e}")

        dpg.set_value("status_text", translator.get_text('delete_success').format(name=cased_overworld_name) + (f"\nReplaced in {replaced_count} maps with {default_ow}." if replaced_count > 0 else ""))

    except Exception as e:
        dpg.set_value("status_text", translator.get_text('delete_error').format(name=overworld_name, error=e))