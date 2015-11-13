#!/usr/bin/env python
__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from Tkinter import *
from collections import OrderedDict
from travian import Travian


# ============================================
# CLASS DEFINITION
# ============================================
class Gui:
    def __init__(self):
        self.pics_path = 'pics/'
        # gui
        self.root = Tk()
        # travian class
        self.travian = Travian(self.root)
        # canvas
        # self.canvas = Canvas(self.root, width=500, height=500)
        # gui items
        self.w = Label(self.root, fg='green')
        self.ress_pics = self.fill_ress_pics()
        self.ress_pic_labels = self.make_ress_pic_labels()
        self.ress_entries = self.make_ress_entries()
        self.vil_label1 = Label(self.root, text='Village 1')
        self.vil_label2 = Label(self.root, text='Village 2')
        self.vil_entry1 = Spinbox(self.root, width=10, justify=CENTER, from_=1, to=self.travian.n_villages, increment=1)
        self.vil_entry2 = Spinbox(self.root, width=10, justify=CENTER, from_=1, to=self.travian.n_villages, increment=1)
        # buttons
        self.buttons = self.create_buttons()

        # self.var = StringVar()
        # self.msg = Message(self.root, textvariable=self.var, width=50)
        # self.dummy = Message()
        # test counter
        self.counter = 0
        self.do_count = False
        # configure gui
        self.config_root()
        self.make_gui()

    def create_buttons(self):
        dic = OrderedDict()
        dic['off'] = Button(self.root, text='On', width=15, command=self.start_count)
        dic['on'] = Button(self.root, text='On', width=15, command=self.stop_count)
        dic['quit'] = Button(self.root, text='Exit', width=15, command=self.root.destroy)
        dic['market'] = Button(self.root, text='Market', width=15, command=self.open_market)
        dic['merchant'] = Button(self.root, text='Send Merchant', width=15, command=self.send_merchant)
        dic['change_vil'] = Button(self.root, text='Change Village', width=15, command=self.change_village)
        return dic

    def open_market(self):
        self.travian.open_market(True)

    def send_merchant(self):
        vil1 = int(self.vil_entry1.get())
        vil2 = int(self.vil_entry2.get())
        ress = []
        for value in self.ress_entries.values():
            ress.append(int(value.get()))
        self.travian.send_merchant(vil1, vil2, ress[0], ress[1], ress[2], ress[3])

    def change_village(self):
        vil = int(self.vil_entry1.get())
        self.travian.change_village(vil, True)

    def config_root(self):
        self.root.title('Travian Helper')
        self.root.geometry('333x333+1400+408')

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
        names = ['lumber', 'clay', 'iron', 'crop']
        for name in names:
            dic[name] = PhotoImage(file='{path}{name}.gif'.format(path=self.pics_path, name=name))
        return dic

    def make_ress_pic_labels(self):
        dic = OrderedDict()
        for key, item in self.ress_pics.iteritems():
            dic[key] = Label(self.root, image=item)
            # num = dic.keys().index(key)
            # dic[key].grid(row=num)
        return dic

    def make_ress_entries(self):
        dic = OrderedDict()
        for key in self.ress_pics:
            dic[key] = Spinbox(self.root, width=10, justify=CENTER, from_=0, to=50000, increment=1000)
        return dic

    def make_gui(self):
        # spinboxes
        for key in self.ress_pics:
            num = self.ress_pics.keys().index(key)
            self.ress_pic_labels[key].grid(row=num)
            self.ress_entries[key].grid(row=num, column=1)
        self.vil_label1.grid(row=4)
        self.vil_label2.grid(row=5)
        self.vil_entry1.grid(row=4, column=1)
        self.vil_entry2.grid(row=5, column=1)
        # buttons
        self.buttons['market'].grid(row=0, column=2, rowspan=2)
        self.buttons['merchant'].grid(row=2, column=2, rowspan=2)
        self.buttons['change_vil'].grid(row=6, columnspan=3)
        self.buttons['quit'].grid(row=7, columnspan=3)

    # def update_message(self):
    #     old = self.var.get()
    #     new = ''
    #     for value in self.ress_entries.values():
    #         # print item
    #         new += value.get() + '\n'
    #     if old != new:
    #         self.var.set(new)
    #         self.msg.after(10, self.update_message)
    #     else:
    #         self.dummy.after(10, self.update_message)











if __name__ == '__main__':
    t = Gui()
    t.count()
    # t.update_message()
    t.root.mainloop()