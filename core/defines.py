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

def update_num_obj_event_gfx():
    base_path = config['pkmn_path']['path']
    file_path = f"{base_path}/include/constants/event_objects.h"

    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_value = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("#define NUM_OBJ_EVENT_GFX"):
            parts = line.split()
            current_value = int(parts[2])
            new_value = current_value + 1
            lines[i] = f"#define NUM_OBJ_EVENT_GFX {new_value}\n"
            break

    with open(file_path, 'w') as file:
        file.writelines(lines)
    return new_value
