# terminal-overlay

# WHY

I like sublime text but it doesn't have a terminal panel, and the Terminus plugin doesn't work well with tmux

So i made this, it lets you use your favorite terminal as an overlay

The terminal will stay above sublime text, but never above other windows

Very useful when debugging your program and reading code at the same time

Or when working on game/server projects

# COMPATIBILITY
- Linux (x11): Yes
- Linux (wayland): no clue, i need to find alternatives for the dependencies
- macOS: me no have this
- windows: me no use this


# DEPENDENCIES
- Linux (x11): 'wmctrl' and 'xdotool'


# HOW TO USE
 - clone this repo in sublime text's Packages folder (File -> Preferenecs -> Browse Packages..)
 - open `overlay.py` and edit the function `start_terminal_command` to use the terminal of your choice 
 - setup a sublime text shortcut for the command `terminal_overlay_toggle`


![image](https://github.com/user-attachments/assets/5b56061f-e1b0-4c14-ac73-dda7d948465f)

![image](https://github.com/user-attachments/assets/e3fc0ca7-4a22-45fb-9992-3cf2fe1ced01)
