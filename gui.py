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

    def create_margin(self, frame):
        label = Label(frame, text=' ', font='font/Font 5')
        return label
