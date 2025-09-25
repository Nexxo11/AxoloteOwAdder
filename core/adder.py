import configparser
import dearpygui.dearpygui as dpg
from core import defines
from utils.file_system import insert_after_line_number, insert_line_in_structure

config = configparser.ConfigParser()
config.read('path.ini')

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

    with open(defines_file, 'r') as f:
        lines = f.readlines()

    endif_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("#endif") and "GUARD_CONSTANTS_EVENT_OBJECTS_H" in line:
            endif_index = i
            break

    if endif_index != -1:
        if project_version == 'Poke-expansion':
            lines.insert(endif_index, f'#define OBJ_EVENT_GFX_{overworld_name.upper()} {next_define_id}\n')
            lines.insert(endif_index + 1, f'#define OBJ_EVENT_PAL_TAG_{overworld_name.upper()} 0x{next_define_hex_id:04X}\n')
        elif project_version == 'Pokeemerald' and dynamic_pal_system == 'True':
            lines.insert(endif_index, f'#define OBJ_EVENT_GFX_{overworld_name.upper()} {next_define_id}\n')
            defines.pokeemerald_pal_define(defines_file, overworld_name.upper())
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
            write_graphics_info(
                f, overworld_name, pal_tag, reflection_palette_tag, size, width, height, palette_slot,
                shadow_size, inanimate, tracks, anim_table, f'.disableReflectionPaletteLoad = {disableReflection},'
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
            if project_version == 'Poke-expansion':
                dpg.set_value("status_text", f"{translator.get_text('overworld_inserted')}\n                          GfxID: {define_overworld_id}  PalID: 0x{define_overworld_hex_id:04X}\n{translator.get_text('num_obj_event_gfx_updated')} {new_value}")
            elif project_version == 'Pokeemerald' and dynamic_pal_system == 'True':
                dpg.set_value("status_text", f"{translator.get_text('overworld_inserted')}\n                          GfxID: {define_overworld_id}  PalID: 0x{defines.define_pal_emerald_hex_id:04X}\n{translator.get_text('num_obj_event_gfx_updated')} {new_value}")
            else:
                dpg.set_value("status_text", f"{translator.get_text('overworld_inserted')}\n                          GfxID: {define_overworld_id}  OBJ_EVENT_PAL_TAG_{pal_tag}\n{translator.get_text('num_obj_event_gfx_updated')} {new_value}")
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
        for line in lines:
            if not in_block and start_str in line:
                in_block = True
                found = True
                # If the last line added was just a blank line, pop it to remove the empty space.
                if new_lines and new_lines[-1].strip() == "":
                    new_lines.pop()
                continue
            if in_block and end_str in line:
                in_block = False
                continue
            if not in_block:
                new_lines.append(line)
        
        if found:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
    except FileNotFoundError:
        pass

def delete_overworld(overworld_name, translator):
    """Main function to delete an overworld and all its references."""
    try:
        if not overworld_exists(overworld_name):
            dpg.set_value("status_text", translator.get_text('delete_not_found').format(name=overworld_name))
            return

        base_path = config['pkmn_path']['path']
        project_version = config['pkmn_path'].get('project_version', 'Pokeemerald')
        dynamic_pal_system = config['pkmn_path'].get('dynamic_pal_system', 'False')

        defines_file = f"{base_path}/include/constants/event_objects.h"
        object_events_file = f"{base_path}/src/data/object_events/object_event_graphics.h"
        pic_tables_file = f"{base_path}/src/data/object_events/object_event_pic_tables.h"
        graphics_info_file = f"{base_path}/src/data/object_events/object_event_graphics_info.h"
        pointers_file = f"{base_path}/src/data/object_events/object_event_graphics_info_pointers.h"
        movement_file = f"{base_path}/src/event_object_movement.c"
        spritesheet_rules_file = f"{base_path}/spritesheet_rules.mk"

        defines_to_remove = [f"OBJ_EVENT_GFX_{overworld_name.upper()}"]
        if project_version == 'Poke-expansion' or dynamic_pal_system == 'True':
            defines_to_remove.append(f"OBJ_EVENT_PAL_TAG_{overworld_name.upper()}")
        _remove_lines_from_file(defines_file, defines_to_remove)

        incbins_to_remove = [f"gObjectEventPic_{overworld_name}[]", f"gObjectEventPal_{overworld_name}[]"]
        _remove_lines_from_file(object_events_file, incbins_to_remove)

        _remove_block_from_file(pic_tables_file, f"sPicTable_{overworld_name}[]")
        _remove_block_from_file(graphics_info_file, f"gObjectEventGraphicsInfo_{overworld_name}")

        pointers_to_remove = [
            f"gObjectEventGraphicsInfo_{overworld_name};",
            f"[OBJ_EVENT_GFX_{overworld_name.upper()}] = &gObjectEventGraphicsInfo_{overworld_name},"
        ]
        _remove_lines_from_file(pointers_file, pointers_to_remove)

        if dynamic_pal_system == 'True' or project_version == 'Poke-expansion':
            _remove_lines_from_file(movement_file, [f"gObjectEventPal_{overworld_name}"])

        with open(spritesheet_rules_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        new_lines = []
        skip_next = False
        for line in lines:
            if skip_next:
                skip_next = False
                continue
            if f"/{overworld_name}.4bpp:" in line:
                skip_next = True
                continue
            new_lines.append(line)
        with open(spritesheet_rules_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        defines.update_num_obj_event_gfx()

        dpg.set_value("status_text", translator.get_text('delete_success').format(name=overworld_name))

    except Exception as e:
        dpg.set_value("status_text", translator.get_text('delete_error').format(name=overworld_name, error=e))