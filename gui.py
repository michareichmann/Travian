#!/usr/bin/env python
__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from Tkinter import *
from collections import OrderedDict


# ============================================
# CLASS DEFINITION
# ============================================
class Gui:

    def __init__(self):
        self.pics_path = 'pics/'
        self.root = Tk()
        self.w = Label(self.root, fg='green')
        self.ress_pics = self.fill_ress_pics()
        self.ress_pic_labels = self.make_ress_pic_labels()
        self.ress_entries = self.make_ress_entries()
        self.w.grid(row=4)
        self.counter = 0
        self.do_count = False
        self.off_button = Button(self.root, text='On', width=15, command=self.start_count)
        self.on_button = Button(self.root, text='Off', width=15, command=self.stop_count)
        self.on_button.grid(row=5)
        self.off_button.grid(row=6)
        self.config_root()

    def config_root(self):
        self.root.title('Travian Helper')

    def count(self):
        if self.do_count:
            self.counter += 1
            self.w.config(text=str(self.counter))
        self.w.after(1000, self.count)

    def stop_count(self):
        self.do_count = False

    def start_count(self):
        self.do_count = True

    def fill_ress_pics(self):
        dic = OrderedDict()
        dic['lumber'] = PhotoImage(file=self.pics_path + 'lumber.gif')
        dic['clay'] = PhotoImage(file=self.pics_path + 'clay.gif')
        dic['iron'] = PhotoImage(file=self.pics_path + 'iron.gif')
        dic['crop'] = PhotoImage(file=self.pics_path + 'crop.gif')
        return dic

    def make_ress_pic_labels(self):
        dic = OrderedDict()
        for key, item in self.ress_pics.iteritems():
            dic[key] = Label(self.root, image=item)
            num = dic.keys().index(key)
            dic[key].grid(row=num)
        return dic

    def make_ress_entries(self):
        dic = OrderedDict()
        for key in self.ress_pics:
            dic[key] = Entry(self.root)
            num = dic.keys().index(key)
            dic[key].grid(row=num, column=1)
            dic[key].insert(10, 0)
        return dic












if __name__ == '__main__':
    t = Gui()
    t.count()
    t.root.mainloop()