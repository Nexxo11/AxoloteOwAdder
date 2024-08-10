# AxoloteOwAdder
# Version 0.3

Is a tool for adding and configuring overworld events in the Pokeemerald-expansion project.
It uses a DearPyGui-based graphical user interface (GUI)

![image](https://github.com/user-attachments/assets/b4c4f3cc-adda-4949-8396-ea648c0103a2)

- Insert and configure overworld events in 2 secs
- Easy to use
- Expansion compatible version 1.9.0

- Python 3.x
- Python libraries: 'tkinter', 'dearpygui', 'configparser'

## Installation

1. Download the Latest Release
    [Download from GitHub Releases](https://github.com/Nexxo11/AxoloteOwAdder/releases)
   False Virus Positive (pyinstaller)

3. Edit event_objects.h
    To support more overworlds, you need to adjust the NUM_OBJ_EVENT_GFX value:
    Open include/constants/event_objects.h.
    Locate the line: #define NUM_OBJ_EVENT_GFX 241.
    Change 241 to the new number required for your Pokeemerald expansion.
    Save the changes to event_objects.h

3. Prepare Your Overworld Sprite
    Paste your indexed (16 colors) overworld sprite into the graphics/object_events/people/ directory.

5. Run AxoloteOwAdder
    Execute the tool and select your Pokeemerald-expansion directory.
    The tool will be ready to use.
