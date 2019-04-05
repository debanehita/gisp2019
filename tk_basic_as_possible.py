"""
Tkinter generic tasks

1. LOOK: Define the look of the screen
2. DO; Define the event handler routines
3. LOOK associated with DO: Associate interesting keyboard events with their handlers.
4. LISTEN: Loop forever, observing events. Exit when an exit event occurs.

"""
from tkinter import *

# Contain top level window usually called root
root = Tk()

# Basic workflow:
# 1. Create a GUI object and associate it with its parent
# 2. Pack it or place it on grid - set up a 'geometry manager'


# Keep listening for events until destroy event occurs.
root.mainloop()

