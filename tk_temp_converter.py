from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class GUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Temperature Converter")

        self.parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        self.main_frame = Frame(self.parent, padx=20, pady=20)
        self.main_frame.grid(row=0, column=0)

        self.choice = IntVar()
        self.result = StringVar()

        self.radio1 = Radiobutton(self.main_frame, text="Fahrenheit to Celsius", variable=self.choice, value=1)
        self.radio2 = Radiobutton(self.main_frame, text="Celsius to Fahrenheit", variable=self.choice, value=2)
        self.radio1.grid(row=0, column=0, columnspan=2, sticky=W)
        self.radio2.grid(row=1, column=0, columnspan=2, sticky=W)

        self.enter_label = Label(self.main_frame, padx=5, pady=5, text="Enter Value")
        self.enter_label.grid(row=2, column=0, sticky=W)

        self.enter_box = Entry(self.main_frame)
        self.enter_box.grid(row=2, column=1, sticky=W)

        self.btn = Button(self.main_frame, text="Convert", command=self.calcuate_result, padx=5, pady=5, bg="red", fg="white")
        self.btn.grid(row=3, column=0, columnspan=2, sticky=W+E)

        self.result_frame = Frame(self.main_frame, padx=10, pady=10, borderwidth=2, relief=SUNKEN)
        self.result_frame.grid(row=4, column=0, columnspan=2, sticky=W+E)
        self.result_label = Label(self.result_frame, padx=5, pady=5, text="Result:")
        self.result_label.grid(row=0, column=0, sticky=W)

        self.result_box = Label(self.result_frame, textvariable=self.result)
        self.result_box.grid(row=0, column=1, sticky=W)


    def calcuate_result(self):
        # Formulae
        # f -> c = (Tf -32) / 1.8
        # c -> f = (Tc * 1.8) +32

        self.result.set(do_non_gui_stuff(self.choice.get(), self.enter_box.get()))
        # try:
        #     if self.choice.get() == 1:
        #         # f -> c
        #         res = (float(self.enter_box.get()) -32) / 1.8
        #         res_str = "{} F = {} C".format(float(self.enter_box.get()), res)
        #         self.result.set(res_str)
        #     elif self.choice.get() == 2:
        #         # c -> f
        #         res = (float(self.enter_box.get()) * 1.8) + 32
        #         res_str = "{} C = {} F".format(float(self.enter_box.get()), res)
        #         self.result.set(res_str)
        #     else:
        #         raise ValueError("You must choose conversion type.")
        # except Exception as e:
        #     messagebox.showerror("Problem!", "{}".format(e))
        #     self.result.set("")


    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()


def do_non_gui_stuff(choice, value):
    try:
        if choice == 1:
            # f -> c
            res = (float(value) - 32) / 1.8
            return "{} F = {} C".format(float(value), res)
        elif choice == 2:
            # c -> f
            res = (float(value) * 1.8) + 32
            return "{} C = {} F".format(float(value), res)
        else:
            raise ValueError("You must choose conversion type.")
    except Exception as e:
        return "Problem!", "{}".format(e)


if __name__ == "__main__":
    root = Tk()
    GUI(root)
    root.mainloop()
