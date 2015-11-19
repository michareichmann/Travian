__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from Tkinter import *
from collections import OrderedDict
from gui import Gui
from travian import Travian


# ============================================
# CLASS DEFINITION
# ============================================
class Raiding(Gui):
    def __init__(self, gui, app):
        Gui.__init__(self)
        # tk
        self.root = gui
        self.travian = app
        # items
        self.news = None
        # frame
        self.frame = Frame(self.root, bd=5, relief=GROOVE)
        # widgets
        self.labels = self.create_labels()
        self.buttons = self.create_buttons()

    # ============================================
    # ITEMS

    # ============================================
    # WIDGETS
    def create_labels(self):
        dic = OrderedDict()
        dic['main'] = self.create_main_label(self.frame, 'Raiding')
        dic['bot'] = self.create_margin(self.frame)
        return dic

    def create_buttons(self):
        dic = OrderedDict()
        dic['all raids'] = Button(self.frame, text='All Raids', width=self.button_size, command=self.travian.send_all_raids)
        return dic

    # ============================================
    # COMMANDS

    # ============================================
    # PACKING
    def make_gui(self):
        self.labels['main'].grid()
        self.buttons['all raids'].grid(row=1, padx=5)



if __name__ == '__main__':
    this_root = Tk()
    travian = Travian(this_root)
    t = Raiding(this_root, travian)
    t.frame.pack()
    t.make_gui()
    t.root.mainloop()
