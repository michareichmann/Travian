#!/usr/bin/env python
__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from pymouse import PyMouse
from time import sleep
from keys import Keys
from glob import glob
from argparse import ArgumentParser
from Tkinter import Tk


class Travian(Keys):
    def __init__(self):
        Keys.__init__(self)
        # tkinter
        self.root = Tk()
        self.root.withdraw()
        # parser
        self.parser = ArgumentParser()
        self.configure_parser()
        self.args = self.parser.parse_args()
        # mouse
        self.m = PyMouse()
        # general stuff
        self.link_list = 5
        self.wait_time = 2
        self.n_troop_sorts = [15, 15, 3]
        self.n_villages = 3
        self.troop_tabs = []
        if self.args.troop_tabs:
            self.get_troop_tabs()
        # self.fill_troop_tabs()
        self.coods = {}
        self.units = ['Clubswinger', 'Scout', 'Ram', 'Chief', 'Spearman', 'Paladin', 'Catapult', 'Settler', 'Axeman', 'Teutonic Knight']
        self.__get_coordinates()
        self.hero = True if self.args.hero else False
        self.hero_village = self.args.hero_village

    def run(self):
        pass

    def open_troops(self, num=0):
        self.goto_init()
        self.wait()
        self.press_tab(26)
        if num:
            self.press_ctrl_enter(num)
        else:
            self.press_enter()

    def goto_init(self):
        self.m.click(65, 125)

    def get_mouse_position(self):
        return self.m.position()

    @staticmethod
    def wait(sec=0.1):
        sleep(sec)

    def open_overview(self):
        """
        Showing Resource overview
        :return:
        """
        self.goto_init()
        self.wait()
        self.press_tab(2)
        self.press_enter()

    def open_map(self):
        """
        Showing Map of the current village
        :return:
        """
        self.goto_init()
        self.wait()
        self.press_tab(4)
        self.press_enter()

    def change_village(self, num):
        self.open_map()
        self.wait(self.wait_time)
        self.press_tab(45 + num)
        self.press_enter()

    def send_raids(self, village=1):
        # goto the village
        assert len(str(village)) < 2, 'wrong village input'
        vil_name = 'village ' + str(village)
        self.change_village(village)
        n_raids = len(self.coods[village]['x'])
        # open tabs
        self.open_troops(n_raids)
        self.wait(n_raids)
        # fill in raid info
        for raids in range(n_raids):
            self.send_raid(1, self.coods[vil_name]['x'][raids], self.coods[vil_name]['y'][raids], self.coods[vil_name]['unit_num'][raids],
                           self.coods[vil_name]['quantity'][raids], False)
            self.wait(0.3)
        # confirm and close tabs
        self.wait(.5 * n_raids)
        for i in range(n_raids):
            self.press_tab(43)
            self.press_enter()
            self.press_ctrl_w()
            self.wait(0.3)

    def send_raid(self, vil_num, x, y, unit_num, quantity, single=True):
        if single:
            self.open_troops()
            self.wait(2)
        else:
            self.press_ctrl_tab()
        n_tabs = self.troop_tabs[vil_num][unit_num]
        self.press_tab(41 + n_tabs)
        self.send_text(quantity)
        self.press_tab(16 - n_tabs)
        self.send_text(x)
        self.press_tab()
        self.send_text(y)
        self.press_tab()
        self.press_down(2)
        self.press_tab()
        self.press_enter()
        if single:
            self.wait(1)
            self.press_tab(43)
            self.press_enter()


    def __get_coordinates(self):
        for name in glob('*.inf'):
            f = open(name, 'r')
            village_name = 'village ' + name[0]
            self.coods[village_name] = {}
            self.coods[village_name]['x'] = []
            self.coods[village_name]['y'] = []
            self.coods[village_name]['unit'] = []
            self.coods[village_name]['unit_num'] = []
            self.coods[village_name]['quantity'] = []
            for line in f:
                data = [int(x) for x in line.split()]
                self.coods[village_name]['x'].append(data[0])
                self.coods[village_name]['y'].append(data[1])
                self.coods[village_name]['unit'].append(self.units[data[2]])
                self.coods[village_name]['unit_num'].append(data[2])
                self.coods[village_name]['quantity'].append(data[3])
        print self.coods

    def configure_parser(self):
        self.parser.add_argument("-H", "--hero", action="store_true", help="True if hero is in village")
        self.parser.add_argument("hero_village", nargs='?', default="2", help="enter the hero village", type=int)
        self.parser.add_argument("-tt", "--troop_tabs", action="store_true", help="read troop tabs from travian")

    def get_troop_tabs(self):
        self.goto_init()
        for j in range(self.n_villages):
            self.change_village(j + 1)
            self.wait(2)
            self.open_troops()
            self.wait(2)
            tabs = [0]
            self.wait()
            self.press_tab(41)
            for i in range(1, 22):
                self.press_tab()
                self.send_text(str(i))
                self.press_shift_left(2)
                self.press_ctrl_and('c')
                self.wait()
                num = self.root.clipboard_get()
                if num == str(i):
                    tabs.append(i)
                if len(tabs) >= 10:
                    break
            self.troop_tabs.append(tabs)
            print j, tabs


if __name__ == '__main__':
    t = Travian()
    # x.run()
