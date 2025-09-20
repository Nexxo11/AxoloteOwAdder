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
            # Check if the structure is empty
            if lines[i+1].strip().startswith("};"):
                lines.insert(i + 1, " " * indent_level + insert_text + '\n')
                break
            else:
                continue

        if inside_structure:
            if insert_position is None:
                if stripped_line.startswith("};"):
                    lines.insert(i, " " * indent_level + insert_text + '\n')
                    break
            else:
                lines.insert(structure_start_index + insert_position + 1, " " * indent_level + insert_text + '\n')
                break

    with open(filename, 'w') as f:
        f.writelines(lines)

