__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from Tkinter import Label


# ============================================
# CLASS DEFINITION
# ============================================
class Gui:
    def __init__(self):
        # gui
        self.dummy = Label()
        self.button_size = 12
        self.pics_path = 'pics/'

    @staticmethod
    def create_margin(frame):
        label = Label(frame, text=' ', font='font/Font 5')
        return label

    @staticmethod
    def create_main_label(frame, txt):
        label = Label(frame, text=txt, font='font/Font 16 bold')
        return label

    def make_gui(self):
        print 'You forgot an implementation here...'
        return
