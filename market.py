__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from Tkinter import *
from collections import OrderedDict
from gui import Gui


# ============================================
# CLASS DEFINITION
# ============================================
class Market(Gui):
    def __init__(self, root):
        Gui.__init__(self)
        # tk
        self.root = root
        # frame
        self.frame = Frame(self.root, bd=5, relief=GROOVE)
        # widgets

