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
    def __init__(self, root, travian):
        Gui.__init__(self)
        # tk
        self.root = root
        self.travian = travian
        # frame
        self.frame = Frame(self.root, bd=5, relief=GROOVE)
        # items
        self.images = self.create_images()
        self.stringvars = self.create_stringvars()
        # widgets

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

    # ============================================
    # WIDGETS

    def create_market_labels(self):
        dic = OrderedDict()
        dic['ress labels'] = self.create_ress_labels()
        dic['vil1'] = Label(self.frame, text='Village 1')
        dic['vil2'] = Label(self.frame, text='Village 2')
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

    def create_market_spin_boxes(self):
        dic = OrderedDict()
        dic['ress'] = OrderedDict()
        for key in self.images:
            dic['ress'][key] = Spinbox(self.frame, width=10, justify=CENTER, from_=0, to=50000, increment=1000)
        return dic

    # ============================================
    # COMMANDS


