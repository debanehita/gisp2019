"""
Tkinter generic tasks

1. LOOK: Define the look of the screen
2. DO; Define the event handler routines
3. LOOK associated with DO: Associate interesting keyboard events with their handlers.
4. LISTEN: Loop forever, observing events. Exit when an exit event occurs.


"""
__author__ = 'mark'

from tkinter import *
from tkinter import messagebox
# from tkinter import filedialog


class MyGUI:
    """
    Class that defines the GUI. This approach helps partition GUI-related elements from other parts of the program.
    Also avoids the use of global variables later.
    Ultimately reduces complexity.
    """

    def __init__(self, my_parent):
        # Basic workflow:
        # 1. Create a GUI object and associate it with its parent
        # 2. Pack it or place it on grid - set up a 'geometry manager'

        # Remember who the parent window is
        self.my_parent = my_parent

        self.my_parent.title("Tk in-class demo")
        # self.my_parent.title.set("Tk in-class demo")

        # Make protocol handler to manage interaction between the application and the window handler
        my_parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        # Create a container to hold the widgets
        self.my_container_1 = Frame(my_parent)
        self.my_container_1.pack()

        self.label = Label(self.my_container_1, text="Tkinter Demo")
        self.label.pack()

        # Create a button object and place it in a container.
        # Note that widgets have attributes.
        self.button1 = Button(self.my_container_1)
        self.button1["text"] = "OK"
        self.button1["background"] = "green"
        self.button1.pack(side=LEFT)

        # Force the button to have 'focus'
        self.button1.focus_force()
        self.button1.bind("<Button-1>", self.button1_click)
        self.button1.bind("<Return>", self.button1_click)

        self.button2 = Button(self.my_container_1)
        self.button2.configure(text="Cancel", background="red")
        self.button2.pack(side=LEFT)
        self.button2.bind("<Button-1>", self.button2_click)
        self.button2.bind("<Return>", self.button2_click)

        # New variants to demo command binding
        self.button3 = Button(self.my_container_1, command=self.button3_click)
        self.button3["text"] = "OK 2"
        self.button3["background"] = "green"
        self.button3.pack(side=LEFT)

        self.button4 = Button(self.my_container_1, command=self.button4_click)
        self.button4.configure(text="Cancel 2", background="red")
        self.button4.pack(side=LEFT)

        self.button5 = Button(self.my_container_1, command=self.button5_click, text="LAMBDA DEMO")
        self.button5.bind("<Button-1>",
                          lambda event, arg1="Lambda Demo", arg2=1, arg3="Good stuff!": self.button5_click(event, arg1,
                                                                                                           arg2, arg3))
        self.button5.pack(side=LEFT)

        # Instance variable to 'remember' between method invocations - much cleaner than global variables
        self.last_button = None


        # Create a container to hold the text box widgets
        self.my_container_2 = Frame(my_parent, padx="5m", pady="5m")
        self.my_container_2.pack()
        # Create a text entry box
        self.text_label = Label(self.my_container_2, text="Enter text:")
        self.text_label.grid(row=0, column=0, sticky=W)
        self.text_input = Entry(self.my_container_2)
        # self.text_input.bind("<Enter>", self.text_input.enter)
        self.text_input.grid(row=0, column=1, sticky=W+E)
        self.text_button = Button(self.my_container_2, text="Get text input", command=self.text_input_enter)
        self.text_button.grid(row=1, column=1, sticky=E)

        self.v = StringVar()
        self.text_result = Label(self.my_container_2, text=None, textvariable=self.v)
        self.text_result.grid(row=2, column=0, sticky=W, columnspan=2)


        # New container
        self.slide_container = Frame(my_parent, padx="5m", pady="5m")
        self.slide_container.pack()

        # Slider
        self.slider = Scale(self.slide_container, from_=0, to=100, orient=HORIZONTAL)
        self.slider.grid(row=0, column=0, sticky=W)
        self.v2 = IntVar()
        self.v2 = self.slider.get()
        self.slide_result = Label(self.my_container_2, text=None, textvariable=self.v2)
        self.slide_result.grid(row=1, column=0, sticky=W)


    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.my_parent.destroy()


    def button1_click(self, event):
        print("Last button: {}".format(self.last_button))
        report_event(event)
        if self.button1["background"] == "green":
            self.button1["background"] = "yellow"
        else:
            self.button1["background"] = "green"

        self.last_button = "button_1"

    def button2_click(self, event):
        report_event(event)
        # self.my_parent.destroy()
        self.catch_destroy()

    def button3_click(self):
        print("button3_click event handler")
        print("Last button: {}".format(self.last_button))
        if self.button3["background"] == "green":
            self.button3["background"] = "yellow"
        else:
            self.button3["background"] = "green"

        self.last_button = "button_3"

    def button4_click(self):
        print("buton4_click event handler")
        self.my_parent.destroy()

    def button5_click(self, *args):
        print("buton5_click event handler")
        for arg in args:
            print("Passed: {}".format(arg))

    def text_input_enter(self):
        self.v.set(self.text_input.get())
        print("You entered: {}".format(self.text_input.get()))


def report_event(event):
    """
    Description of an event based on its attributes
    :param event:
    :return:
    """

    event_name = {"2": "KeyPress", "4": "ButtonPress"}
    print("Time: {}".format(str(event.time)))
    print("Type: {} {}  WidgetId: {}  KeySymbol: {}".format(str(event.type), event_name[str(event.type)],
                                                            str(event.widget), str(event.keysym)))


def main():
    # Contain top level window usually called root
    root = Tk()

    # # Can run file dialogue from anywhere
    # chosen_file = filedialog.askopenfilename(filetypes=(("Template files", "*.tplate"),
    #                                                     ("HTML files", "*.html;*.htm"),
    #                                                     ("All files", "*.*") ))
    # print("Selected: {}".format(chosen_file))

    # Create an instance of the class that defines the GUI and associate it with the top level window..
    MyGUI(root)
    # Keep listening for events until destroy event occurs.
    root.mainloop()


if __name__ == "__main__":
    main()