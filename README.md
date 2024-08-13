# AxoloteOwAdder
# Version 0.3.2

Is a tool for adding and configuring overworld events in the Pokeemerald

![image](https://github.com/user-attachments/assets/afd40f40-25c9-4284-a16e-bf0d9cea5224)
![image](https://github.com/user-attachments/assets/57e493b1-8778-4446-a972-672ef68b5895)

- Insert and configure overworld events in 2 secs
- Easy to use

## Installation

1. Download the Latest Release
    [Download from GitHub Releases](https://github.com/Nexxo11/AxoloteOwAdder/releases)
   False Virus Positive (pyinstaller)

2. Edit event_objects.h
    To support more overworlds, you need to adjust the NUM_OBJ_EVENT_GFX value:
    Open include/constants/event_objects.h.
    Locate the line: #define NUM_OBJ_EVENT_GFX 241.
    Change 241 to the new number required for your Pokeemerald expansion.
    Save the changes to event_objects.h

3. Run AxoloteOwAdder
    Execute the tool and select your Project directory.
    The tool will be ready to use.

## Build
1. Install pyinstaller

2. Use this command

   pyinstaller --noconfirm --onedir --windowed --icon "AxoloteOwAdder\icon.ico" --name "AxoloteOwAdder" --add-data "AxoloteOwAdder\src;src/"  "AxoloteOwAdder\ui.py"
