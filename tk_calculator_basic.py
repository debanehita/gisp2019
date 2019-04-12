"""
Tkinter generic tasks

1. LOOK: Define the look of the screen
2. DO; Define the event handler routines
3. LOOK associated with DO: Associate interesting keyboard events with their handlers.
4. LISTEN: Loop forever, observing events. Exit when an exit event occurs.


"""

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext as tkst
from tkinter import font


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

        self.parent = my_parent

        self.parent.title("Basic Calculator")

        # Make protocol handler to manage interaction between the application and the window handler
        self.parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        # Set up fonts for text area
        arial_bold = font.Font(family="Arial", size=14, weight=font.BOLD)
        arial_normal = font.Font(family="Arial", size=14, weight=font.NORMAL)

        # GUI layout
        self.main_frame = ttk.Frame(my_parent)
        self.main_frame.grid(row=0, column=0)
        self.frame1 = ttk.Frame(self.main_frame, border=1)
        self.frame1.grid(row=0, column=0, padx=5, pady=5, )
        self.frame2 = ttk.Frame(self.main_frame, border=1)
        self.frame2.grid(row=1, column=0, padx=5, pady=5)
        self.frame21 = ttk.Frame(self.frame2)
        self.frame21.grid(row=0, column=0, sticky=NW, padx=10, pady=10)
        self.frame22 = ttk.Frame(self.frame2)
        self.frame22.grid(row=0, column=1, sticky=NE, padx=10, pady=10)

        # Must not accept keyboard input
        # Must insert each element from button press
        # Must reflect result from '='
        self.textwin = tkst.ScrolledText(
            self.frame1,
            background="lightgrey",
            wrap=WORD,
            height=15,
            width=50,
        )
        self.textwin.tag_configure("rj", justify=RIGHT)
        self.textwin.tag_configure("ab", font=arial_bold)
        self.textwin.tag_configure("an", font=arial_normal)
        self.textwin.grid(row=0, column=0)

        # Buttons all call the same function.We use lambda to enable us to pass the value of the button to the function
        self.btn_7 = Button(self.frame21, width=3, height=3,
                            bg="black", fg="white",
                            text="7", command=lambda btn="7": self.btn_pressed(btn)) \
            .grid(row=0, column=0)
        self.btn_8 = Button(self.frame21, width=3, height=3,
                            bg="black", fg="white",
                            text="8", command=lambda btn="8": self.btn_pressed(btn)) \
            .grid(row=0, column=1)
        self.btn_9 = Button(self.frame21, width=3, height=3,
                            bg="black", fg="white",
                            text="9", command=lambda btn="9": self.btn_pressed(btn)) \
            .grid(row=0, column=2)
        self.btn_4 = Button(self.frame21, width=3, height=3,
                            bg="black", fg="white",
                            text="4", command=lambda btn="4": self.btn_pressed(btn)) \
            .grid(row=1, column=0)
        self.btn_5 = Button(self.frame21, width=3, height=3,
                            bg="black", fg="white",
                            text="5", command=lambda btn="5": self.btn_pressed(btn)) \
            .grid(row=1, column=1)
        self.btn_6 = Button(self.frame21, width=3, height=3,
                            bg="black", fg="white",
                            text="6", command=lambda btn="6": self.btn_pressed(btn)) \
            .grid(row=1, column=2)
        self.btn_1 = Button(self.frame21, width=3, height=3,
                            bg="black", fg="white",
                            text="1", command=lambda btn="1": self.btn_pressed(btn)) \
            .grid(row=2, column=0)
        self.btn_2 = Button(self.frame21, width=3, height=3,
                            bg="black", fg="white",
                            text="2", command=lambda btn="2": self.btn_pressed(btn)) \
            .grid(row=2, column=1)
        self.btn_3 = Button(self.frame21, width=3, height=3,
                            bg="black", fg="white",
                            text="3", command=lambda btn="3": self.btn_pressed(btn)) \
            .grid(row=2, column=2)
        self.btn_0 = Button(self.frame21, width=3, height=3,
                            bg="black", fg="white",
                            text="0", command=lambda btn="0": self.btn_pressed(btn)) \
            .grid(row=3, column=0)
        self.btn_decimal = Button(self.frame21, width=3, height=3,
                                  bg="black", fg="white",
                                  text=".", command=lambda btn=".": self.btn_pressed(btn)) \
            .grid(row=3, column=2)

        self.btn_clear = Button(self.frame22, width=3, height=3,
                                bg="red", fg="white",
                                text="Clear", command=self.btn_clear_pressed) \
            .grid(row=0, column=0, columnspan=2, sticky=W + E)
        self.btn_add = Button(self.frame22, width=3, height=3,
                              bg="black", fg="white",
                              text="+", command=lambda btn="+": self.btn_pressed(btn)) \
            .grid(row=1, column=0)
        self.btn_sub = Button(self.frame22, width=3, height=3,
                              bg="black", fg="white",
                              text="-", command=lambda btn="-": self.btn_pressed(btn)) \
            .grid(row=1, column=1)
        self.btn_mul = Button(self.frame22, width=3, height=3,
                              bg="black", fg="white",
                              text="X", command=lambda btn="*": self.btn_pressed(btn)) \
            .grid(row=2, column=0)
        self.btn_div = Button(self.frame22, width=3, height=3,
                              bg="black", fg="white",
                              text="/", command=lambda btn="/": self.btn_pressed(btn)) \
            .grid(row=2, column=1)
        self.btn_eq = Button(self.frame22, width=3, height=3,
                             bg="black", fg="white",
                             text="=", command=self.btn_eq_pressed) \
            .grid(row=3, column=0, columnspan=2, sticky=W + E)

        # We construct a calculation string which we will 'eval' later
        self.current_calc_string = ""
        # Keep tarck of how many times we pressed a button for this line. Helps with formatting the calc string in the
        # text area
        self.btn_count = 0

    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()

    def btn_clear_pressed(self):
        self.textwin.delete(1.0, END, )
        self.current_calc_string = ""
        self.btn_count = 0

    def btn_eq_pressed(self):
        result = ""
        try:
            # Do the calculation
            result = "{}".format(eval(self.current_calc_string))
        except Exception as e:
            result = "{}".format(e)
        finally:
            self.textwin.insert("1.50", "=", "rj an")
            self.textwin.insert("1.0", "{}\n".format(result), "rj ab")
            self.current_calc_string = ""
            self.btn_count = 0

    def btn_pressed(self, btn):
        if self.btn_count == 0:
            self.textwin.insert("1.0", "\n")
        self.current_calc_string += btn
        self.textwin.insert("1.50", btn, "rj an")
        self.btn_count += 1


def main():
    # Contain top level window usually called root
    root = Tk()
    # Create an instance of the class that defines the GUI and associate it with the top level window..
    my_gui = MyGUI(root)
    # Keep listening for events until destroy event occurs.
    root.mainloop()


if __name__ == "__main__":
    main()
