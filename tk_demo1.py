"""
Tkinter generic tasks

1. LOOK: Define the look of the screen
2. DO; Define the event handler routines
3. LOOK associated with DO: Associate interesting keyboard events with their handlers.
4. LISTEN: Loop forever, observing events. Exit when an exit event occurs.


"""
__author__ = 'mark'

from tkinter import *

# Contain top level window usually called root
root = Tk()

# Basic workflow:
# 1. Create a GUI object and associate it with its parent
# 2. Pack it or place it on grid - set up a 'geometry manager'

my_container_1 = Frame(root)
my_container_1.pack()

# Create a button object and place it in a container.
# Note that widgets have attributes.
my_button = Button(my_container_1)
my_button["text"] = "Hello World!"
my_button["background"] = "green"
my_button.pack()

# Keep listening for events until destroy event occurs.
root.mainloop()

