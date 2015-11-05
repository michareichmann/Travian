#!/usr/bin/env python
__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from pymouse import PyMouse
# from pykeyboard import PyKeyboard
from time import sleep
from keys import Keys
from glob import glob


class Travian(Keys):

    def __init__(self):
        Keys.__init__(self)
        self.m = PyMouse()
        self.link_list = 5
        self.wait_time = 2
        self.n_troop_sorts = [15, 15, 3]
        self.n_villages = 3
        self.troop_tabs = []
        self.fill_troop_tabs()
        self.coods = {}
        self.units = ['Clubswinger', 'Scout', 'Ram', 'Chief', 'Spearman', 'Paladin', 'Catapult', 'Settler', 'Axeman', 'Teutonic Knight']
        self.__get_coordinates()


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
        self.m.click(1943, 125)

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

    def change_village(self, num):
        self.open_overview()
        self.wait(self.wait_time)
        self.press_tab(71 + num)
        self.press_enter()

    def send_raids(self):
        n_raids = len(self.coods['village 2']['x'])
        # open tabs
        self.open_troops(n_raids)
        self.wait(n_raids)
        # fill in raid info
        for raids in range(n_raids):
            # self.press_ctrl_tab()
            # unit_num = self.coods['village 2']['unit_num'][raids]
            # n_tabs = self.troop_tabs[1][unit_num]
            # self.press_tab(41 + n_tabs)
            # self.send_text(self.coods['village 2']['quantity'][raids])
            # self.press_tab(16 - n_tabs)
            # self.send_text(self.coods['village 2']['x'][raids])
            # self.press_tab()
            # self.send_text(self.coods['village 2']['y'][raids])
            # self.press_tab()
            # self.press_down(2)
            # self.press_tab()
            # self.press_enter()
            self.send_raid(1, self.coods['village 2']['x'][raids], self.coods['village 2']['y'][raids], self.coods['village 2']['unit_num'][raids], self.coods['village 2']['quantity'][raids], False)
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


    # def get_n_tabs(self, unit, village):


    def fill_troop_tabs(self):
        self.troop_tabs = [x for x in self.n_troop_sorts]
        self.troop_tabs[1] = [0, 2, 4, 5, 6, 8, 10, 11, 12, 13]


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








if __name__ == '__main__':
    x = Travian()
    # x.run()
