__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from Tkinter import *
# from collections import OrderedDict
from gui import Gui
from travian import Travian
from send_frame import Send
from offer_frame import Offer


# ============================================
# CLASS DEFINITION
# ============================================
class Market(Gui):
    def __init__(self, mark_root, mark_travian):
        Gui.__init__(self)
        # tk
        self.root = mark_root
        # frame
        self.frame = Frame(self.root, bd=5, relief=GROOVE)
        # subframes
        self.send = Send(mark_root, mark_travian)
        self.offer = Offer(mark_root, mark_travian)
        # widgets
        self.label = Label(self.frame, text='Marketplace', font='font/Font 16 bold')
        self.margin = self.create_margin(self.frame)

    def make_gui(self):
        self.label.grid(columnspan=3)
        self.send.frame.grid(in_=self.frame, row=1)
        self.send.make_gui()
        self.margin.grid(row=1, column=1)
        self.offer.frame.grid(in_=self.frame, row=1, column=2, sticky='NEWS')
        self.offer.make_gui()



if __name__ == '__main__':
    this_root = Tk()
    travian = Travian(this_root)
    t = Market(this_root, travian)
    t.frame.pack()
    t.make_gui()
    t.root.mainloop()
