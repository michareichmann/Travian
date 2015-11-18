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

    def make_gui(self):
        self.send.frame.pack(in_=self.frame, side=LEFT)
        self.send.make_gui()
        self.offer.frame.pack(in_=self.frame, side=LEFT, anchor=CENTER)
        self.offer.make_gui()



if __name__ == '__main__':
    this_root = Tk()
    travian = Travian(this_root)
    t = Market(this_root, travian)
    t.frame.pack()
    t.make_gui()
    t.root.mainloop()