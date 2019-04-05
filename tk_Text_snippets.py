from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext as tkst
from tkinter import font

# Set up fonts for text area
arial_bold = font.Font(family="Arial", size=14, weight=font.BOLD)
arial_normal = font.Font(family="Arial", size=14, weight=font.NORMAL)

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

