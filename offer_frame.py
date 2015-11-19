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
class Offer(Gui):
    def __init__(self, gui, app):
        Gui.__init__(self)
        # tk
        self.root = gui
        self.travian = app
        # frames
        self.frame = Frame(self.root)
        # items
        self.news = None
        self.resources = ['Lumber', 'Clay', 'Iron', 'Crop']
        self.stringvars = self.create_stringvars()
        self.intvars = self.create_intvars()
        # widgets
        self.labels = self.create_labels()
        self.buttons = self.create_buttons()
        self.opt_menus = self.create_opt_menus()
        self.spin_boxes = self.create_spin_boxes()
        self.check_buttons = self.create_check_buttons()

    # ============================================
    # ITEMS
    def create_stringvars(self):
        dic = OrderedDict()
        dic['res1'] = StringVar()
        dic['res2'] = StringVar()
        dic['vil'] = StringVar()
        dic['res1'].set('Lumber')
        dic['res2'].set('Clay')
        dic['vil'].set(self.travian.villages.keys()[0])
        dic['terminal'] = StringVar()
        dic['terminal'].set('Message Box')
        return dic

    @staticmethod
    def create_intvars():
        dic = OrderedDict()
        dic['ally'] = IntVar()
        dic['max time'] = IntVar()
        dic['max time'].set(1)
        return dic

    # ============================================
    # WIDGETS
    def create_buttons(self):
        dic = OrderedDict()
        dic['offer'] = Button(self.frame, text='Make Offer', width=self.button_size, command=self.make_offer)
        return dic

    def create_opt_menus(self):
        dic_opt = OrderedDict()
        dic_opt['res1'] = OptionMenu(self.frame, self.stringvars['res1'], *self.resources)
        dic_opt['res2'] = OptionMenu(self.frame, self.stringvars['res2'], *self.resources)
        dic_opt['vil'] = OptionMenu(self.frame, self.stringvars['vil'], *self.travian.villages.keys())
        dic_opt['res1'].configure(width=6)
        dic_opt['res2'].configure(width=6)
        dic_opt['vil'].configure(width=8)
        return dic_opt

    def create_spin_boxes(self):
        dic = OrderedDict()
        dic['res1'] = Spinbox(self.frame, width=10, justify=CENTER, from_=1000, to=10000, increment=1000)
        dic['res2'] = Spinbox(self.frame, width=10, justify=CENTER, from_=1000, to=10000, increment=1000)
        dic['num'] = Spinbox(self.frame, width=3, justify=CENTER, from_=1, to=20, increment=1)
        dic['max time'] = Spinbox(self.frame, width=3, justify=CENTER, from_=1, to=20, increment=1)
        dic['max time'].delete(0, 'end')
        dic['max time'].insert(0, 4)
        return dic

    def create_labels(self):
        dic = OrderedDict()
        dic['main'] = Label(self.frame, text='Make Offer', font='font/Font 12 bold')
        dic['num'] = Label(self.frame, text='x')
        dic['vil'] = Label(self.frame, text='Village:')
        return dic

    def create_check_buttons(self):
        dic = OrderedDict()
        dic['ally'] = Checkbutton(self.frame, text='ally', variable=self.intvars['ally'])
        dic['max time'] = Checkbutton(self.frame, text='max time', width=8, variable=self.intvars['max time'])
        return dic

    # ============================================
    # COMMANDS
    def make_offer(self):
        vil = self.stringvars['vil'].get()
        res1 = self.stringvars['res1'].get()
        res2 = self.stringvars['res2'].get()
        quant1 = self.spin_boxes['res1'].get()
        quant2 = self.spin_boxes['res2'].get()
        num = int(self.spin_boxes['num'].get())
        ally = bool(self.intvars['ally'].get())
        max_time = bool(self.intvars['max time'].get())
        max_num = int(self.spin_boxes['max time'].get())
        self.travian.market_offer(vil, res1, res2, quant1, quant2, num, max_time, max_num, ally)

    # ============================================
    # PACKING
    def make_gui(self):
        # self.frame.pack(in_=parent_frame)
        self.labels['main'].grid(pady=5, columnspan=5)
        self.opt_menus['res1'].grid(row=1, columnspan=2)
        self.opt_menus['res2'].grid(row=2, columnspan=2)
        self.spin_boxes['res1'].grid(row=1, column=2, ipady=4, columnspan=3, sticky=E)
        self.spin_boxes['res2'].grid(row=2, column=2, ipady=4, columnspan=3, sticky=E)
        self.check_buttons['ally'].grid(row=3)
        self.check_buttons['max time'].grid(row=3, column=1, columnspan=3, padx=10, sticky=E)
        self.spin_boxes['max time'].grid(row=3, column=4, sticky=E)
        self.labels['vil'].grid(row=4, columnspan=2)
        self.opt_menus['vil'].grid(row=4, column=2, columnspan=3)
        self.buttons['offer'].grid(row=5, columnspan=3, pady=2)
        self.labels['num'].grid(row=5, column=3, padx=6)
        self.spin_boxes['num'].grid(row=5, column=4)


if __name__ == '__main__':
    this_root = Tk()
    travian = Travian(this_root)
    t = Offer(this_root, travian)
    t.frame.pack()
    t.make_gui()
    t.root.mainloop()
