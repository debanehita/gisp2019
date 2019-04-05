"""
Tkinter generic tasks

1. LOOK: Define the look of the screen
2. DO; Define the event handler routines
3. LOOK associated with DO: Associate interesting keyboard events with their handlers.
4. LISTEN: Loop forever, observing events. Exit when an exit event occurs.


"""
__author__ = 'mark'

from tkinter import *


class MyGUI:
    """
    Class that defines the GUI. This approach helps partition GUI-related elements
    from other parts of the program. Also avoids the use of global variables later.
    Ultimately reduces complexity.
    """

    def __init__(self, my_parent):
        # Basic workflow:
        # 1. Create a GUI object and associate it with its parent
        # 2. Pack it or place it on grid - set up a 'geometry manager'

        self.my_container_1 = Frame(my_parent)
        self.my_container_1.pack()

        # Create a button object and place it in a container.
        # Note that widgets have attributes.
        self.my_button = Button(self.my_container_1)
        self.my_button["text"] = "Hello World!"
        self.my_button["background"] = "green"
        self.my_button.pack(side=LEFT)
        self.my_button.bind("<Button-1>", self.print_random)

        self.button2 = Button(self.my_container_1)
        self.button2.configure(text="Off to join the circus!", background="Tan")
        self.button2.pack(side=LEFT)

        self.my_container_2 = Toplevel(my_parent)
        self.my_container_2.title("a separate t/level win")
        self.my_container_3 = Frame(self.my_container_2)
        self.my_container_3.pack()
        self.lablel1 = Label(self.my_container_3)
        self.lablel1["text"] = "some text in a label"
        self.lablel1.pack()

    def print_random(self, evt):
        print("random stuff")


def main():
    # Contain top level window usually called root
    root = Tk()
    # Create an instance of the class that defines the GUI and associate it with the top level window..
    MyGUI(root)
    # Keep listening for events until destroy event occurs.
    root.mainloop()


if __name__ == "__main__":
    main()
