import configparser

config = configparser.ConfigParser()
config.read('path.ini')

define_pal_emerald_hex_id = 0

def get_next_define_number(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
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

def get_next_pal_tag_define_number(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
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

def pokeemerald_pal_define(file_path, overworld_name):
    next_define_hex_id = get_next_pal_tag_define_number(file_path)
    
    global define_pal_emerald_hex_id
    define_pal_emerald_hex_id = next_define_hex_id

    with open(file_path, 'r+', encoding='utf-8') as f:
        lines = f.readlines()

    endif_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("#endif") and "GUARD_CONSTANTS_EVENT_OBJECTS_H" in line:
            endif_index = i
            break
            
    # Fallback
    if endif_index == -1:
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith("#endif"):
                endif_index = i
                break

    if endif_index != -1:
        new_line = f"#define OBJ_EVENT_PAL_TAG_{overworld_name.upper()} 0x{next_define_hex_id:04X}\n"
        lines.insert(endif_index, new_line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def update_num_obj_event_gfx(increment=True):
    base_path = config['pkmn_path']['path']
    file_path = f"{base_path}/include/constants/event_objects.h"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return -1

    # Find the highest ID among all OBJ_EVENT_GFX_ defines
    max_id = 0
    num_gfx_line_index = -1
    
    for i, line in enumerate(lines):
        line_strip = line.strip()
        if line_strip.startswith("#define NUM_OBJ_EVENT_GFX"):
            num_gfx_line_index = i
            continue
            
        if line_strip.startswith("#define OBJ_EVENT_GFX_"):
            parts = line_strip.split()
            if len(parts) >= 3:
                try:
                    val = int(parts[2])
                    if val > max_id:
                        max_id = val
                except ValueError:
                    pass

    # The new NUM_OBJ_EVENT_GFX should be max_id + 1
    new_value = max_id + 1

    if num_gfx_line_index != -1:
        # Update the line
        current_line = lines[num_gfx_line_index]
        parts = current_line.split()
        if len(parts) >= 3:
            # Reconstruct line preserving possible comments? 
            # Usually it's just "#define NUM_OBJ_EVENT_GFX Value"
            # But let's safe replace just the number
            import re
            try:
                current_val = int(parts[2])
                lines[num_gfx_line_index] = re.sub(r'\b' + str(current_val) + r'\b', str(new_value), current_line, count=1)
            except ValueError:
                # Fallback if parsing failed
                lines[num_gfx_line_index] = f"#define NUM_OBJ_EVENT_GFX {new_value}\n"
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
            
    return new_value
