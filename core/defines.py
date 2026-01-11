import configparser

config = configparser.ConfigParser()
config.read('path.ini')

define_pal_emerald_hex_id = 0

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

def get_next_pal_tag_define_number(file_path):
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

def pokeemerald_pal_define(file_path, overworld_name):
    next_define_hex_id = get_next_pal_tag_define_number(file_path)
    
    global define_pal_emerald_hex_id
    define_pal_emerald_hex_id = next_define_hex_id

    with open(file_path, 'r+') as f:
        lines = f.readlines()

    endif_index = -1
    for i, line in enumerate(lines):
        if line.strip() == "#endif // GUARD_CONSTANTS_EVENT_OBJECTS_H":
            endif_index = i
            break

    if endif_index != -1:
        new_line = f"#define OBJ_EVENT_PAL_TAG_{overworld_name.upper()} 0x{next_define_hex_id:04X}\n"
        lines.insert(endif_index, new_line)

    with open(file_path, 'w') as f:
        f.writelines(lines)

def update_num_obj_event_gfx(increment=True):
    base_path = config['pkmn_path']['path']
    file_path = f"{base_path}/include/constants/event_objects.h"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return -1

    num_gfx_line_index = -1
    current_value = -1
    
    for i, line in enumerate(lines):
        if line.strip().startswith("#define NUM_OBJ_EVENT_GFX"):
            num_gfx_line_index = i
            # Extract the current number using split
            parts = line.split()
            if len(parts) >= 3:
                try:
                    # Clean potential comments or extra text in the line
                    val_str = parts[2].strip()
                    current_value = int(val_str)
                except ValueError:
                    pass
            break

    new_value = -1
    if num_gfx_line_index != -1 and current_value != -1:
        new_value = current_value + 1 if increment else current_value - 1
        # Replace the value in the line, preserving the rest of the line (like spacing/comments)
        import re
        lines[num_gfx_line_index] = re.sub(r'\b' + str(current_value) + r'\b', str(new_value), lines[num_gfx_line_index])
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
            
    return new_value
