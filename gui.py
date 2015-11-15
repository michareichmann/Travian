#!/usr/bin/env python
__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from Tkinter import *
from collections import OrderedDict
from travian import Travian
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
        # Mail.__init__(self)
        self.pics_path = 'pics/'
        # gui
        self.root = Tk()
        # travian class
        self.travian = Travian(self.root)
        # frames
        self.main_frame = Frame(self.root)
        self.market_frame = Frame(self.root, bd=5, relief=GROOVE)
        self.raid_frame = Frame(self.root, bd=5, relief=GROOVE)
        self.info_frame = Frame(self.root, bd=5, relief=GROOVE)
        # gui items
        # variables
        self.info_vars = self.create_info_vars()
        # pics
        self.pics = self.create_pics()
        # labels
        self.market_labels = self.create_market_labels()
        self.raid_labels = self.create_raid_labels()
        self.info_labels = self.create_info_labels()
        self.dummy = Label()
        # spin boxes
        self.spin_boxes = self.create_spin_boxes()
        self.info_spin_boxes = self.create_info_spinboxes()
        # option menus
        self.option_vars = self.create_option_vars()
        self.opt_menus = self.create_opt_menus()
        # buttons
        self.market_buttons = self.create_market_buttons()
        self.raid_buttons = self.create_raid_buttons()
        self.info_buttons = self.create_info_buttons()
        self.buttons = self.create_buttons()
        # bools
        self.gather_attack_info = False
        self.flash_bg = False
        # tmp
        # configure gui
        self.config_root()
        self.make_market_frame()
        self.make_raid_frame()
        self.make_info_frame()

    # ============================================
    # OBJECT CREATION
    # region object creation
    def create_buttons(self):
        dic = OrderedDict()
        dic['restart'] = Button(self.raid_frame, text='Restart', width=button_size, command=self.restart)
        dic['quit'] = Button(self.raid_frame, text='Exit', width=button_size, command=self.root.destroy)
        return dic

    def create_market_buttons(self):
        dic = OrderedDict()
        # dic['off'] = Button(self.market_frame, text='On', width=15, command=self.start_count)
        # dic['on'] = Button(self.market_frame, text='On', width=15, command=self.stop_count)
        dic['market'] = Button(self.market_frame, text='Market', width=button_size, command=self.open_market)
        dic['merchant'] = Button(self.market_frame, text='Send Merchant', width=button_size, command=self.send_merchant)
        dic['change_vil'] = Button(self.market_frame, text='Change Village', width=button_size, command=self.change_village)
        dic['clear'] = Button(self.market_frame, text='Clear', width=15, command=self.clear)
        return dic

    def create_raid_buttons(self):
        dic = OrderedDict()
        dic['all raids'] = Button(self.raid_frame, text='All Raids', width=button_size, command=self.travian.send_all_raids)
        return dic

    def create_info_buttons(self):
        dic = OrderedDict()
        dic['status'] = Button(self.info_frame, text='ON', font='font/Font 10 bold', width=5, relief=GROOVE, bd=4, command=self.switch_attack_status)
        # dic['off'] = Button(self.info_frame, text='OFF', font='font/Font 10 bold', width=5, relief=GROOVE, bd=4, command=self.stop_update_attacks)
        return dic

    def create_info_vars(self):
        dic = OrderedDict()
        dic['attacks'] = OrderedDict()
        for key, vil in self.travian.villages.iteritems():
            dic['attacks'][key] = StringVar()
            dic['attacks'][key].set('-')
        dic['status'] = StringVar()
        dic['status'].set('OFF')
        return dic

    def create_option_vars(self):
        dic = OrderedDict()
        dic['vil1'] = StringVar()
        dic['vil2'] = StringVar()
        dic['vil1'].set(self.travian.villages.keys()[0])
        dic['vil2'].set(self.travian.villages.keys()[1])
        return dic

    def create_opt_menus(self):
        dic_opt = OrderedDict()
        dic_opt['vil1'] = OptionMenu(self.market_frame, self.option_vars['vil1'], *self.travian.villages.keys())
        dic_opt['vil2'] = OptionMenu(self.market_frame, self.option_vars['vil2'], *self.travian.villages.keys())
        dic_opt['vil1'].configure(width=8)
        dic_opt['vil2'].configure(width=8)
        return dic_opt

    def create_market_labels(self):
        dic = OrderedDict()
        dic['ress labels'] = self.create_ress_labels()
        dic['vil1'] = Label(self.market_frame, text='Village 1')
        dic['vil2'] = Label(self.market_frame, text='Village 2')
        dic['main'] = Label(self.market_frame, text='Marketplace', font='font/Font 16 bold')
        dic['bot'] = Label(self.market_frame, text=' ', font='font/Font 5')
        return dic

    def create_raid_labels(self):
        dic = OrderedDict()
        dic['main'] = Label(self.raid_frame, text='Raid Manager', font='font/Font 16 bold')
        dic['bot'] = Label(self.raid_frame, text=' ', font='font/Font 5')
        return dic

    def create_info_labels(self):
        dic = OrderedDict()
        dic['main'] = Label(self.info_frame, text='Info Frame', font='font/Font 16 bold')
        dic['attacks'] = OrderedDict()
        for key in self.travian.villages:
            dic['attacks'][key] = tuple([Label(self.info_frame, text=key, anchor=W, width=10), Label(self.info_frame, textvar=self.info_vars['attacks'][key])])
        dic['bot'] = Label(self.info_frame, text=' ', font='font/Font 5')
        dic['update time'] = Label(self.info_frame, text='Update time:', anchor=E)
        dic['tag'] = Label(self.info_frame, text='Attacks', font='font/Font 10 bold')
        dic['status'] = Label(self.info_frame, textvar=self.info_vars['status'], font='font/Font 10 bold', width=5)
        return dic

    def create_pics(self):
        dic = OrderedDict()
        names = ['lumber', 'clay', 'iron', 'crop']
        for name in names:
            dic[name] = PhotoImage(file='{path}{name}.gif'.format(path=self.pics_path, name=name))
        return dic

    def create_ress_labels(self):
        dic = OrderedDict()
        for key, item in self.pics.iteritems():
            dic[key] = Label(self.market_frame, image=item)
            # num = dic.keys().index(key)
            # dic[key].grid(row=num)
        return dic

    def create_spin_boxes(self):
        dic = OrderedDict()
        for key in self.pics:
            dic[key] = Spinbox(self.market_frame, width=10, justify=CENTER, from_=0, to=50000, increment=1000)
        return dic

    def create_info_spinboxes(self):
        dic = OrderedDict()
        dic['update time'] = Spinbox(self.info_frame, width=3, justify=CENTER, from_=10, to=100, increment=10)
        return dic
    # endregion

    # ============================================
    # COMMANDS
    # region commands
    def open_market(self):
        self.travian.open_market(True)

    def send_merchant(self):
        vil1 = self.option_vars['vil1'].get()
        vil2 = self.option_vars['vil2'].get()
        ress = []
        for value in self.spin_boxes.values():
            ress.append(int(value.get()))
        self.travian.send_merchant(vil1, vil2, ress[0], ress[1], ress[2], ress[3])

    def change_village(self):
        vil = self.option_vars['vil1'].get()
        vil_num = self.travian.villages.keys().index(vil) + 1
        self.travian.change_village(vil_num, True)

    def clear(self):
        for box in self.spin_boxes.values():
            box.delete(0, 'end')
            box.insert(0, 0)

    def config_root(self):
        self.root.title('Travian Helper')
        self.root.geometry('+600-80')  # 530x400

    def restart(self):
        self.root.destroy()
        python = executable
        execl(python, python, *argv)

    def switch_attack_status(self):
        if self.gather_attack_info:
            self.gather_attack_info = False
            self.info_vars['status'].set('OFF')
            self.info_labels['status'].configure(fg='black')
            self.info_buttons['status'].configure(text='ON')
        else:
            self.gather_attack_info = True
            self.info_vars['status'].set('ON')
            self.info_labels['status'].configure(fg='red')
            self.info_buttons['status'].configure(text='OFF')

    # def stop_update_attacks(self):
    #     self.gather_attack_info = False
    #     self.info_vars['status'].set('OFF')
    #     self.info_labels['status'].configure(fg='black')

    def update_attacks(self):
        update_time = int(self.info_spin_boxes['update time'].get()) * 1000
        if self.gather_attack_info:
            self.travian.acquire_stat_info()
            i = 0
            for var, info in zip(self.info_vars['attacks'].values(), self.travian.villages.values()):
                lab = self.info_labels['attacks'].values()[i][1]
                if info['attacks in'] > 0:
                    lab.configure(fg='red')
                else:
                    lab.configure(fg='black')
                var.set(info['attacks in'])
                # print var.get()
            self.travian.press_alt_tab()
            self.info_labels['attacks'].values()[0][0].after(update_time, self.update_attacks)
        else:
            self.dummy.after(update_time, self.update_attacks)

    def flash_status(self):
        label = self.info_labels['status']
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

    # def count(self):
    #     if self.do_count:
    #         self.counter += 1
    #         self.w.config(text=str(self.counter))
    #     self.w.after(1000, self.count)

    # def stop_count(self):
    #     self.do_count = False
    #
    # def start_count(self):
    #     self.do_count = True
    #  endregion

    # ============================================
    # FRAMES AND PACKING
    def make_market_frame(self):
        self.market_frame.grid()
        # spinboxes
        self.market_labels['main'].grid(columnspan=3, pady=10)
        for key in self.pics:
            num = self.pics.keys().index(key)
            self.market_labels['ress labels'][key].grid(row=num + 1)
            self.spin_boxes[key].grid(row=num + 1, column=1)
        self.market_buttons['clear'].grid(row=5, columnspan=2)
        self.market_labels['vil1'].grid(row=6, pady=10, sticky=S)
        self.market_labels['vil2'].grid(row=7)
        self.opt_menus['vil1'].grid(row=6, column=1)
        self.opt_menus['vil2'].grid(row=7, column=1)
        # buttons
        self.market_buttons['market'].grid(row=1, column=2, rowspan=2, padx=15)
        self.market_buttons['merchant'].grid(row=3, column=2, rowspan=2)
        self.market_buttons['change_vil'].grid(row=5, column=2)
        self.market_labels['bot'].grid(row=8)

    def make_raid_frame(self):
        self.raid_frame.grid(row=0, column=1, sticky=N + E + W + S)
        self.raid_frame.grid_rowconfigure(1, weight=1)
        self.raid_labels['main'].grid(padx=20, pady=10)
        self.raid_buttons['all raids'].grid(row=1)
        self.buttons['restart'].grid(row=2, sticky=S)
        self.buttons['quit'].grid(row=3, sticky=S)
        self.raid_labels['bot'].grid(row=4)

    def make_info_frame(self):
        self.info_frame.grid(row=1, columnspan=2, sticky='NEWS')
        self.info_labels['main'].grid(columnspan=7, pady=10)
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(6, weight=1)
        self.info_labels['tag'].grid(row=1, column=2)
        i = 2
        for label in self.info_labels['attacks'].values():
            label[0].grid(row=i, column=1)
            label[1].grid(row=i, column=2)
            i += 1
        self.info_buttons['status'].grid(row=3, column=3, rowspan=2, columnspan=2, padx=40)
        # self.info_buttons['off'].grid(row=4, column=3, rowspan=2, columnspan=2)
        self.info_labels['bot'].grid(row=6)
        self.info_labels['update time'].grid(row=1, column=3, sticky=E)
        self.info_spin_boxes['update time'].grid(row=1, column=4, pady=8, sticky=W)
        self.info_labels['status'].grid(row=1, column=5, pady=4, sticky=E)

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
    t.update_attacks()
    t.flash_status()
    t.root.mainloop()
