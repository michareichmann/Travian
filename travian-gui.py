#!/usr/bin/env python
__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from Tkinter import *
from collections import OrderedDict
from travian import Travian
from market import Market
from raid_frame import Raiding
from info_frame import Info
from os import execl
from sys import executable, argv
# from mail import Mail

# ============================================
# CONSTANTS
# ============================================
button_size = 12


# ============================================
# CLASS DEFINITION
# ============================================
class Gui:
    def __init__(self):
        # gui
        self.root = Tk()
        # compositions
        self.travian = Travian(self.root)
        self.market = Market(self.root, self.travian)
        self.raiding = Raiding(self.root, self.travian)
        self.info = Info(self.root, self.travian)
        # self.mail = Mail()
        # frames
        self.main_frame = Frame(self.root)
        # items
        # widgets
        self.buttons = self.create_buttons()
        # configure gui
        self.config_root()
        self.make_market_frame()
        self.make_raid_frame()
        self.make_info_frame()

    # ============================================
    # region WIDGETS
    def create_buttons(self):
        dic = OrderedDict()
        dic['restart'] = Button(self.raiding.frame, text='Restart', width=button_size, command=self.restart)
        dic['quit'] = Button(self.raiding.frame, text='Exit', width=button_size, command=self.root.destroy)
        return dic

    # ============================================
    # region COMMANDS
    def config_root(self):
        self.root.title('Travian Helper')
        self.root.geometry('+600-80')  # 530x400

    def restart(self):
        self.root.destroy()
        python = executable
        execl(python, python, *argv)
    #  endregion

    # ============================================
    # region FRAMES AND PACKING

    def make_market_frame(self):
        self.market.frame.grid()
        self.market.make_gui()

    def make_raid_frame(self):
        self.raiding.frame.grid(row=0, column=1, sticky='NEWS')
        self.raiding.frame.grid_rowconfigure(1, weight=1)
        self.raiding.make_gui()

    def make_info_frame(self):
        self.info.frame.grid(row=1, columnspan=2, sticky='NEWS')
        self.info.make_gui()
    # endregion

    def do_nothing(self):
        pass


if __name__ == '__main__':
    t = Gui()
    t.info.update_attacks()
    t.info.flash_status()
    t.root.mainloop()
