# AxoloteOwAdder
# Version 0.2.1

Is a tool for adding and configuring overworld events in the Pokeemerald-expansion project.
It uses a DearPyGui-based graphical user interface (GUI)

![image](https://github.com/user-attachments/assets/95d1c0cf-07ba-4879-b260-f067c62bb7b6)

- Insert and configure overworld events in 2 secs
- Easy to use
- Expansion compatible version 1.9.0

- Python 3.x
- Python libraries: 'tkinter', 'dearpygui', 'configparser'

## Installation

1. Clone the repository:
    git clone https://github.com/Nexxo11/AxoloteOwAdder.git
    
2. Edit event_objects.h:
    To use more overworlds, you need to adjust the NUM_OBJ_EVENT_GFX value. Follow these steps:

    Go to include/constants/event_objects.h and locate the line:
    #define NUM_OBJ_EVENT_GFX 241

    Change 241 to the new number required for your Pokeemerald expansion.

    Save the changes to event_objects.h.

4. Paste your indexed (16 colors) overworld sprite into the graphics/object_events/people/ directory.

3. Run AxoloteOwAdder:
    Execute the tool and select your Pokeemerald-expansion directory. 
    The tool will be ready to use.
