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
class Info(Gui):
    def __init__(self, gui, app):
        Gui.__init__(self)
        # tk
        self.root = gui
        self.travian = app
        # frame
        self.frame = Frame(self.root, bd=5, relief=GROOVE)
        # items
        self.news = None
        self.stringvars = self.create_stringvars()
        # widgets
        self.labels = self.create_labels()
        self.buttons = self.create_buttons()
        self.spinboxes = self.create_spinboxes()
        # bools
        self.gather_attack_info = False
        self.flash_bg = False

    # ============================================
    # ITEMS
    def create_stringvars(self):
        dic = OrderedDict()
        dic['attacks'] = OrderedDict()
        for key, vil in self.travian.villages.iteritems():
            dic['attacks'][key] = StringVar()
            dic['attacks'][key].set('-')
        dic['status'] = StringVar()
        dic['status'].set('OFF')
        return dic
    
    # ============================================
    # WIDGETS
    def create_buttons(self):
        dic = OrderedDict()
        dic['status'] = Button(self.frame, text='ON', font='font/Font 10 bold', width=5, relief=GROOVE, bd=4, command=self.switch_attack_status)
        return dic
    
    def create_labels(self):
        dic = OrderedDict()
        dic['main'] = Label(self.frame, text='Info Frame', font='font/Font 16 bold')
        dic['attacks'] = OrderedDict()
        for key in self.travian.villages:
            dic['attacks'][key] = tuple([Label(self.frame, text=key, anchor=W, width=10), Label(self.frame, textvar=self.stringvars['attacks'][key])])
        dic['bot'] = Label(self.frame, text=' ', font='font/Font 5')
        dic['update time'] = Label(self.frame, text='Update time:', anchor=E)
        dic['tag'] = Label(self.frame, text='Attacks', font='font/Font 10 bold')
        dic['status'] = Label(self.frame, textvar=self.stringvars['status'], font='font/Font 10 bold', width=5)
        return dic

    def create_spinboxes(self):
        dic = OrderedDict()
        dic['update time'] = Spinbox(self.frame, width=3, justify=CENTER, from_=5, to=100, increment=5)
        return dic

    # ============================================
    # COMMANDS
    def switch_attack_status(self):
        if self.gather_attack_info:
            self.gather_attack_info = False
            self.stringvars['status'].set('OFF')
            self.labels['status'].configure(fg='black')
            self.buttons['status'].configure(text='ON')
        else:
            self.gather_attack_info = True
            self.stringvars['status'].set('ON')
            self.labels['status'].configure(fg='red')
            self.buttons['status'].configure(text='OFF')

    def update_attacks(self):
        update_time = int(self.spinboxes['update time'].get()) * 1000
        if self.gather_attack_info:
            self.travian.acquire_stat_info()
            i = 0
            for var, info in zip(self.stringvars['attacks'].values(), self.travian.villages.values()):
                lab = self.labels['attacks'].values()[i][1]
                if info['attacks in'] > 0:
                    lab.configure(fg='red')
                else:
                    lab.configure(fg='black')
                var.set(info['attacks in'])
                # print var.get()
            self.travian.press_alt_tab()
            self.labels['attacks'].values()[0][0].after(update_time, self.update_attacks)
        else:
            self.dummy.after(update_time, self.update_attacks)

    def flash_status(self):
        label = self.labels['status']
        if self.gather_attack_info:
            bg = label.cget('background')
            if self.flash_bg:
                label.configure(fg=bg)
                self.flash_bg = False
            else:
                label.configure(fg='red')
                self.flash_bg = True
        else:
            label.configure(fg='black')
        label.after(500, self.flash_status)

    # ============================================
    # PACKING
    def make_gui(self):
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(6, weight=1)
        self.labels['main'].grid(columnspan=7, pady=10)
        self.labels['tag'].grid(row=1, column=2)
        i = 2
        for label in self.labels['attacks'].values():
            label[0].grid(row=i, column=1)
            label[1].grid(row=i, column=2)
            i += 1
        self.buttons['status'].grid(row=3, column=3, rowspan=2, columnspan=2, padx=40)
        # self.info_buttons['off'].grid(row=4, column=3, rowspan=2, columnspan=2)
        self.labels['bot'].grid(row=6)
        self.labels['update time'].grid(row=1, column=3, sticky=E)
        self.spinboxes['update time'].grid(row=1, column=4, pady=8, sticky=W)
        self.labels['status'].grid(row=1, column=5, pady=4, sticky=E)


if __name__ == '__main__':
    this_root = Tk()
    travian = Travian(this_root)
    t = Info(this_root, travian)
    t.frame.pack()
    t.make_gui()
    t.update_attacks()
    t.flash_status()
    t.root.mainloop()
