import configparser
import shutil
import os
import threading
import dearpygui.dearpygui as dpg
from core import defines
from utils.file_system import insert_after_line_number, insert_line_in_structure

config = configparser.ConfigParser()
config.read('path.ini')

def create_backups(file_paths):
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                shutil.copy(file_path, f"{file_path}.bak")
        except Exception as e:
            print(f"Warning: Could not create backup for {file_path}: {e}")

def restore_backups(translator):
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

    with open(defines_file, 'r', encoding='utf-8') as f:
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

    with open(defines_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    with open(object_events_file, 'a', encoding='utf-8') as f:
        f.write(f'const u32 gObjectEventPic_{overworld_name}[] = INCBIN_U32("graphics/object_events/pics/people/{overworld_name}.4bpp");\n')
        if dynamic_pal_system == 'True' or project_version == 'Poke-expansion':
            f.write(f'const u16 gObjectEventPal_{overworld_name}[] = INCBIN_U16("graphics/object_events/pics/people/{overworld_name}.gbapal");\n')

    frames = "\n".join([f'    overworld_frame(gObjectEventPic_{overworld_name}, {width//8}, {height//8}, {i}),' for i in range(frame_num)])
    with open(pic_tables_file, 'a', encoding='utf-8') as f:
                f.write(f'\nstatic const struct SpriteFrameImage sPicTable_{overworld_name}[] = {{{frames}}};')

    with open(graphics_info_file, 'a', encoding='utf-8') as f:
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

    with open(spritesheet_rules_file, 'a', encoding='utf-8') as f:
        f.write(f'\n$(OBJEVENTGFXDIR)/people/{overworld_name}.4bpp: %.4bpp: %.png\n')
        f.write(f'\t$(GFX) $< $@ -mwidth {width//8} -mheight {height//8}\n')

def overworld_exists(overworld_name):
    config.read('path.ini')
    base_path = config['pkmn_path']['path']
    defines_file = f"{base_path}/include/constants/event_objects.h"
    
    # Normalize input for agnostic comparison
    norm_input = overworld_name.lower().replace("_", "")
    
    try:
        with open(defines_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all OBJ_EVENT_GFX_ defines and compare normalized
        matches = re.findall(r'#define\s+(OBJ_EVENT_GFX_\w+)', content)
        for m in matches:
            norm_m = m.replace("OBJ_EVENT_GFX_", "").lower().replace("_", "")
            if norm_m == norm_input:
                return True
    except Exception:
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

        with open('path.ini', 'w', encoding='utf-8') as configfile:
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

def replace_in_file(file_path, target_string, replacement_string):
    """
    Replaces a specific string with a replacement string in a given file.
    Uses regex for word boundary safety.
    Returns True if a replacement was made.
    """
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Use regex for safety with word boundaries
        pattern = r'\b' + re.escape(target_string) + r'\b'
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement_string, content)
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(new_content)
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return False

def scan_and_replace_references(root_dir, target_define, replacement_define, extensions=None, progress_tag=None, text_tag=None):
    """
    Recursively scans a directory for files with specific extensions and replaces a target define.
    """
    if extensions is None:
        extensions = [".c", ".h", ".inc", ".s"]
    
    if not os.path.exists(root_dir):
        return 0

    if text_tag:
        dpg.set_value(text_tag, f"Collecting files in {os.path.basename(root_dir)}...")

    # Collect files first for progress bar
    files_to_process = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                # Exclude the constant definition file
                if "include/constants/event_objects.h" in file_path.replace("\\", "/"):
                    continue
                files_to_process.append(file_path)

    total = len(files_to_process)
    count = 0
    for i, file_path in enumerate(files_to_process):
        if progress_tag and total > 0:
            dpg.set_value(progress_tag, (i / total))
        
        if text_tag and i % 5 == 0: # Update text occasionally to show life
            percent = int((i / total) * 100) if total > 0 else 0
            dpg.set_value(text_tag, f"Scanning {os.path.basename(root_dir)}... {percent}% ({i}/{total})")

        if replace_in_file(file_path, target_define, replacement_define):
            count += 1
            
    return count

def replace_map_references(base_path, target_define, replacement_define, progress_tag=None, text_tag=None):
    """
    Scans data/maps for map.json and events.inc and replaces the target define.
    Updates a DPG progress bar if progress_tag is provided.
    """
    maps_dir = os.path.join(base_path, "data", "maps")
    
    if not os.path.exists(maps_dir):
        return 0

    if text_tag:
        dpg.set_value(text_tag, "Collecting map files...")

    # First, gather all files to process to calculate total for progress bar
    files_to_process = []
    for root, dirs, files in os.walk(maps_dir):
        for file in files:
            if file in ["map.json", "events.inc"]:
                files_to_process.append(os.path.join(root, file))

    total_files = len(files_to_process)
    count = 0

    # Walk through the collected files
    for i, file_path in enumerate(files_to_process):
        # Update progress
        if progress_tag and total_files > 0:
            dpg.set_value(progress_tag, (i / total_files))

        if text_tag and i % 5 == 0:
            percent = int((i / total_files) * 100) if total_files > 0 else 0
            dpg.set_value(text_tag, f"Scanning maps... {percent}% ({i}/{total_files})")

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if target_define in content:
                # Replace word boundary to ensure exact match
                pattern = r'\b' + re.escape(target_define) + r'\b'
                if re.search(pattern, content):
                    new_content = re.sub(pattern, replacement_define, content)
                    with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(new_content)
                    count += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
    if progress_tag:
        dpg.set_value(progress_tag, 1.0)

        
    return count

def _get_cased_overworld_name(base_path, overworld_name):
    """
    Attempts to find the exact casing of the overworld name as used in
    object_event_graphics.h (e.g. gObjectEventPic_Name).
    Returns the found name (with case) or the original if not found.
    Ignores underscores during comparison to handle 'Girl_2' vs 'Girl2' mismatches.
    """
    object_events_file = f"{base_path}/src/data/object_events/object_event_graphics.h"
    try:
        with open(object_events_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Normalize input: remove underscores, lower case
        normalized_input = overworld_name.lower().replace("_", "")
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
                        # Normalize found name
                        normalized_found = found_name.lower().replace("_", "")
                        
                        if normalized_found == normalized_input:
                            return found_name
    except FileNotFoundError:
        pass
    
    return overworld_name

def _remove_lines_with_regex(file_path, patterns_to_find):
    """
    Removes lines matching any of the given regex patterns (case-insensitive).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        # Compile patterns with IGNORECASE
        compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns_to_find]
        
        original_len = len(lines)
        for line in lines:
            if not any(cp.search(line) for cp in compiled_patterns):
                new_lines.append(line)
        
        if len(new_lines) < original_len:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
    except FileNotFoundError:
        pass

def _remove_block_with_regex(file_path, start_pattern, end_str="}};"):
    """
    Removes a block of code starting with a line matching start_pattern (regex)
    and ending with end_str. Handles single-line blocks correctly.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        in_block = False
        found = False
        skip_next_empty = False
        
        start_re = re.compile(start_pattern, re.IGNORECASE)

        for line in lines:
            if skip_next_empty:
                skip_next_empty = False
                if line.strip() == "":
                    continue

            # Check if this line marks the start of the block
            if not in_block and start_re.search(line):
                found = True
                
                # Check if it is a single-line block (starts and ends on same line)
                if end_str in line:
                    # It's a one-liner. Just skip this line.
                    # Remove preceding blank line if last added line was blank
                    if new_lines and new_lines[-1].strip() == "":
                        new_lines.pop()
                    continue
                else:
                    # Multi-line block start
                    in_block = True
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

def find_associated_define(base_path, overworld_name):
    """
    Scans object_event_graphics_info_pointers.h to find the define used for the given overworld.
    Returns the define name (e.g. 'OBJ_EVENT_GFX_GIRL_3') or None.
    """
    pointers_file = os.path.join(base_path, "src", "data", "object_events", "object_event_graphics_info_pointers.h")
    target_struct = f"gObjectEventGraphicsInfo_{overworld_name}"
    
    try:
        with open(pointers_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for [DEFINE_NAME] = &gObjectEventGraphicsInfo_Name
        # Use regex to capture the define
        pattern = rf"\[\s*(OBJ_EVENT_GFX_\w+)\s*\]\s*=\s*&{re.escape(target_struct)}"
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

def _delete_overworld_task(overworld_name, translator):

    """

    Background task to perform the deletion logic.

    """

    try:

        with open("delete_debug.log", "w") as log:

            log.write(f"Starting deletion for: '{overworld_name}'\n")

    except:

        pass



    def log_msg(msg):

        try:

            with open("delete_debug.log", "a") as log:

                log.write(msg + "\n")

        except:

            pass



    try:

        if not overworld_exists(overworld_name):

            log_msg("Overworld does not exist according to overworld_exists")

            dpg.set_value("status_text", translator.get_text('delete_not_found').format(name=overworld_name))

            return



        base_path = config['pkmn_path']['path']

        log_msg(f"Base path: {base_path}")

        

        # Resolve casing (Agnostic to underscores)

        cased_overworld_name = _get_cased_overworld_name(base_path, overworld_name)

        log_msg(f"Cased name: {cased_overworld_name}")



        # Find the actual define used (Crucial for map replacement)

        found_define = find_associated_define(base_path, cased_overworld_name)

        log_msg(f"Found define in pointers: {found_define}")

        

        # Determine the define to use for deletion and replacement

        define_name_to_use = found_define if found_define else f"OBJ_EVENT_GFX_{cased_overworld_name.upper()}"

        log_msg(f"Define to use: {define_name_to_use}")



        # Replace references in maps

        dpg.set_value("loading_text", "Scanning maps for references...")

        default_ow = find_default_overworld(base_path, cased_overworld_name)

        log_msg(f"Default replacement: {default_ow}")

        # Pass the EXACT define found (or constructed) to be replaced
        replaced_count = replace_map_references(base_path, define_name_to_use, default_ow, progress_tag="progress_bar", text_tag="loading_text")
        log_msg(f"Replaced maps: {replaced_count}")

        # Scan src/ for lingering references (battle tower, pike, contest, etc.)
        dpg.set_value("loading_text", "Scanning src/ for references...")
        src_dir = os.path.join(base_path, "src")
        replaced_src_count = scan_and_replace_references(src_dir, define_name_to_use, default_ow, progress_tag="progress_bar", text_tag="loading_text")
        log_msg(f"Replaced references in src/: {replaced_src_count}")

        # Scan include/ for lingering references
        dpg.set_value("loading_text", "Scanning include/ for references...")
        include_dir = os.path.join(base_path, "include")
        replaced_inc_count = scan_and_replace_references(include_dir, define_name_to_use, default_ow, progress_tag="progress_bar", text_tag="loading_text")
        log_msg(f"Replaced references in include/: {replaced_inc_count}")

        # Scan data/ for lingering references (outside maps)
        dpg.set_value("loading_text", "Scanning data/ for references...")
        data_dir = os.path.join(base_path, "data")
        replaced_data_count = scan_and_replace_references(data_dir, define_name_to_use, default_ow, progress_tag="progress_bar", text_tag="loading_text")
        log_msg(f"Replaced references in data/: {replaced_data_count}")



        # Update text for file deletion

        dpg.set_value("loading_text", "Removing files and updating tables...")

        dpg.set_value("progress_bar", 1.0) 

        

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



        # Use regex for defines

        defines_patterns = [

            rf"#define\s+{re.escape(define_name_to_use)}\b",

            rf"#define\s+{re.escape(define_name_to_use.replace('OBJ_EVENT_GFX', 'OBJ_EVENT_PAL_TAG'))}\b",

            rf"#define\s+OBJ_EVENT_GFX_{re.escape(cased_overworld_name.upper())}\b",

            rf"#define\s+OBJ_EVENT_PAL_TAG_{re.escape(cased_overworld_name.upper())}\b"

        ]

        log_msg(f"Defining patterns: {defines_patterns}")

        _remove_lines_with_regex(defines_file, defines_patterns)



        # Remove INCBINs

        incbins_patterns = [

            rf"gObjectEventPic_{re.escape(cased_overworld_name)}\[\]", 

            rf"gObjectEventPal_{re.escape(cased_overworld_name)}\[\]"

        ]

        log_msg(f"Incbins patterns: {incbins_patterns}")

        _remove_lines_with_regex(object_events_file, incbins_patterns)



        # Remove blocks

        log_msg("Removing blocks...")

        _remove_block_with_regex(pic_tables_file, rf"sPicTable_{re.escape(cased_overworld_name)}\[\]", end_str="};")

        _remove_block_with_regex(graphics_info_file, rf"gObjectEventGraphicsInfo_{re.escape(cased_overworld_name)}\b", end_str="};")



        # Remove pointers

        pointers_patterns = [

            rf"gObjectEventGraphicsInfo_{re.escape(cased_overworld_name)}\b",

            rf"\[{re.escape(define_name_to_use)}\]"

        ]

        log_msg(f"Pointers patterns: {pointers_patterns}")

        _remove_lines_with_regex(pointers_file, pointers_patterns)



        # Remove from movement file

        movement_patterns = [rf"gObjectEventPal_{re.escape(cased_overworld_name)}\b"]

        _remove_lines_with_regex(movement_file, movement_patterns)



        # Remove rule

        with open(spritesheet_rules_file, 'r', encoding='utf-8') as f:

            lines = f.readlines()

        new_lines = []

        skip_next = False

        target_rule = f"/{cased_overworld_name}.4bpp:".lower()

        log_msg(f"Target rule: {target_rule}")

        

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

        for img_file in image_files:

            if os.path.exists(img_file):

                try:

                    os.remove(img_file)

                    log_msg(f"Removed image: {img_file}")

                except Exception as e:

                    print(f"Warning: Could not remove {img_file}: {e}")

                    log_msg(f"Error removing image {img_file}: {e}")



        success_msg = translator.get_text('delete_success').format(name=cased_overworld_name) + (f"\nReplaced in {replaced_count} maps with {default_ow}." if replaced_count > 0 else "")

        dpg.set_value("status_text", success_msg)

        log_msg("Success.")



    except Exception as e:

        import traceback

        error_msg = f"{e}\n{traceback.format_exc()}"

        log_msg(f"EXCEPTION: {error_msg}")

        dpg.set_value("status_text", translator.get_text('delete_error').format(name=overworld_name, error=e))

    finally:

        if dpg.does_item_exist("loading_modal"):

            dpg.delete_item("loading_modal")



def delete_overworld(overworld_name, translator):

    overworld_name = overworld_name.strip()

    with dpg.window(label="Status", modal=True, show=True, tag="loading_modal", width=400, height=120, no_close=True):

        dpg.add_text(translator.get_text('processing_maps') if hasattr(translator, 'get_text') else "Processing maps and references...", tag="loading_text")

        dpg.add_progress_bar(tag="progress_bar", default_value=0.0, width=380)

    threading.Thread(target=_delete_overworld_task, args=(overworld_name, translator), daemon=True).start()