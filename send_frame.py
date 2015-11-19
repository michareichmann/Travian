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
class Send(Gui):
    def __init__(self, gui, app):
        Gui.__init__(self)
        # tk
        self.root = gui
        self.travian = app
        # frames
        self.frame = Frame(self.root)
        # items
        self.news = None
        self.images = self.create_images()
        self.stringvars = self.create_stringvars()
        self.intvars = self.create_intvars()
        # widgets
        self.buttons = self.create_buttons()
        self.labels = self.create_labels()
        self.opt_menus = self.create_opt_menus()
        self.spin_boxes = self.create_spin_boxes()
        self.check_buttons = self.create_check_buttons()

    # ============================================
    # ITEMS
    def create_stringvars(self):
        dic = OrderedDict()
        dic['vil1'] = StringVar()
        dic['vil2'] = StringVar()
        dic['vil1'].set(self.travian.villages.keys()[0])
        dic['vil2'].set(self.travian.villages.keys()[1])
        return dic

    def create_images(self):
        dic = OrderedDict()
        names = ['Lumber', 'Clay', 'Iron', 'Crop']
        for name in names:
            dic[name] = PhotoImage(file='{path}{name}.gif'.format(path=self.pics_path, name=name.lower()))
        return dic

    @staticmethod
    def create_intvars():
        dic = OrderedDict()
        dic['go twice'] = IntVar()
        return dic

    # ============================================
    # WIDGETS
    def create_buttons(self):
        dic = OrderedDict()
        dic['market'] = Button(self.frame, text='Market', width=self.button_size, command=self.open_market)
        dic['merchant'] = Button(self.frame, text='Send Merchant', width=self.button_size, command=self.send_merchant)
        dic['clear'] = Button(self.frame, text='Clear', width=10, command=self.clear)
        return dic

    def create_labels(self):
        dic = OrderedDict()
        dic['main'] = Label(self.frame, text='Send Merchants', font='font/Font 12 bold')
        dic['ress'] = self.create_ress_labels()
        dic['vil1'] = Label(self.frame, text='From:')
        dic['vil2'] = Label(self.frame, text='To:')
        return dic

    def create_ress_labels(self):
        dic = OrderedDict()
        for key, item in self.images.iteritems():
            dic[key] = Label(self.frame, image=item)
        return dic

    def create_opt_menus(self):
        dic_opt = OrderedDict()
        dic_opt['vil1'] = OptionMenu(self.frame, self.stringvars['vil1'], *self.travian.villages.keys())
        dic_opt['vil2'] = OptionMenu(self.frame, self.stringvars['vil2'], *self.travian.villages.keys())
        dic_opt['vil1'].configure(width=8)
        dic_opt['vil2'].configure(width=8)
        return dic_opt

    def create_spin_boxes(self):
        dic = OrderedDict()
        dic['ress'] = OrderedDict()
        for key in self.images:
            dic['ress'][key] = Spinbox(self.frame, width=10, justify=CENTER, from_=0, to=50000, increment=1000)
        return dic

    def create_check_buttons(self):
        dic = OrderedDict()
        dic['go twice'] = Checkbutton(self.frame, text='go twice', variable=self.intvars['go twice'])
        return dic

    # ============================================
    # COMMANDS
    def open_market(self):
        self.travian.open_market(True)

    def send_merchant(self):
        vil1 = self.stringvars['vil1'].get()
        vil2 = self.stringvars['vil2'].get()
        ress = []
        for value in self.spin_boxes['ress'].values():
            ress.append(int(value.get()))
        go_twice = bool(self.intvars['go twice'].get())
        message = self.travian.send_merchant(vil1, vil2, ress[0], ress[1], ress[2], ress[3], go_twice)
        if message:
            self.news = message
        self.travian.open_previous_window()

    def clear(self):
        for box in self.spin_boxes['ress'].values():
            box.delete(0, 'end')
            box.insert(0, 0)

    # ============================================
    # PACKING
    def make_gui(self):
        # self.frame.pack(in_=parent_frame)
        row = 0
        self.labels['main'].grid(pady=5, columnspan=2)
        for row, key in enumerate(self.images.keys(), 1):
            self.labels['ress'][key].grid(row=row)
            self.spin_boxes['ress'][key].grid(row=row, column=1)
        self.buttons['clear'].grid(row=row + 1, column=1, pady=2)
        self.labels['vil1'].grid(row=row + 2)
        self.opt_menus['vil1'].grid(row=row + 2, column=1)
        self.labels['vil2'].grid(row=row + 3)
        self.opt_menus['vil2'].grid(row=row + 3, column=1)
        self.check_buttons['go twice'].grid(row=row + 4, columnspan=2)
        self.buttons['merchant'].grid(row=row + 5, columnspan=2, pady=2)


if __name__ == '__main__':
    this_root = Tk()
    travian = Travian(this_root)
    t = Send(this_root, travian)
    t.frame.pack()
    t.make_gui()
    t.root.mainloop()
