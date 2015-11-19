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
# CLASS DEFINITION
# ============================================
# class TravianGui(Gui):
class TravianGui:
    def __init__(self):
        # Gui.__init__(self)
        # gui
        self.root = Tk()
        # compositions
        self.travian = Travian(self.root)
        self.market = Market(self.root, self.travian)
        self.raiding = Raiding(self.root, self.travian)
        self.info = Info(self.root, self.travian)
        # self.mail = Mail()
        # frames
        self.exit_frame = Frame(self.root, bd=5, relief=GROOVE)
        # items
        self.intvars = self.create_intvars()
        self.msg_var = StringVar()
        self.msg_var.set('Messages')
        self.old_news = self.create_news()
        self.news = self.create_news()
        # widgets
        self.buttons = self.create_buttons()
        self.checkboxes = self.create_checkboxes()
        self.messages = self.create_messages()
        # configure gui
        self.config_root()
        self.make_market_frame()
        self.make_raid_frame()
        self.make_info_frame()
        self.make_exit_frame()

    # ============================================
    # region ITEMS
    @staticmethod
    def create_intvars():
        dic = OrderedDict()
        dic['sitter'] = IntVar()
        return dic

    def create_news(self):
        dic = OrderedDict()
        dic['send'] = self.market.send.news
        dic['offer'] = self.market.offer.news
        dic['raid'] = self.raiding.news
        dic['info'] = self.info.news
        return dic

    # ============================================
    # region WIDGETS
    def create_buttons(self):
        dic = OrderedDict()
        dic['restart'] = Button(self.exit_frame, text='Restart', width=self.info.button_size, command=self.restart)
        dic['quit'] = Button(self.exit_frame, text='Exit', width=self.info.button_size, command=self.root.destroy)
        return dic

    def create_checkboxes(self):
        dic = OrderedDict()
        dic['sitter'] = Checkbutton(self.exit_frame, text='sitter', variable=self.intvars['sitter'], command=self.set_sitter)
        return dic

    def create_messages(self):
        dic = OrderedDict()
        dic['terminal'] = Message(self.market.offer.frame, textvar=self.msg_var, bg='bisque3', font='times 12', relief=SUNKEN)
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

    def set_sitter(self):
        is_sitter = bool(self.intvars['sitter'].get())
        return self.travian.sitter_mode(is_sitter)

    def message_handler(self):
        self.news = self.create_news()
        for key, value in self.news.iteritems():
            if value != self.old_news[key]:
                self.msg_var.set(value)
                self.old_news[key] = value
        self.messages['terminal'].after(100, self.message_handler)
    #  endregion

    # ============================================
    # region FRAMES AND PACKING
    def make_market_frame(self):
        self.market.frame.grid()
        self.market.make_gui()
        self.messages['terminal'].grid(row=6, columnspan=5, sticky='NEWS', pady=2, padx=2)
        self.market.offer.frame.grid_rowconfigure(6, weight=1)

    def make_raid_frame(self):
        self.raiding.frame.grid(row=0, column=1, sticky='NEWS')
        self.raiding.frame.grid_rowconfigure(1, weight=1)
        self.raiding.make_gui()

    def make_info_frame(self):
        self.info.frame.grid(row=1, columnspan=2, sticky='NEWS')
        self.info.make_gui()

    def make_exit_frame(self):
        self.exit_frame.grid(row=2, columnspan=2, sticky='NEWS')
        self.exit_frame.grid_columnconfigure(0, weight=1)
        self.exit_frame.grid_columnconfigure(1, weight=1)
        self.exit_frame.grid_columnconfigure(2, weight=1)
        self.checkboxes['sitter'].grid(row=0)
        self.buttons['restart'].grid(row=0, column=1, pady=6)
        self.buttons['quit'].grid(row=0, column=2)
    # endregion

    def do_nothing(self):
        pass


if __name__ == '__main__':
    t = TravianGui()
    t.info.update_attacks()
    t.info.flash_status()
    t.message_handler()
    t.root.mainloop()
