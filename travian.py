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
import pickle
import os.path
from collections import OrderedDict


# ============================================
# MAIN CLASS DEFINITION
# ============================================
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
        self.suppress_xlib_output()
        # general stuff
        self.link_list = 5
        self.wait_time = 2
        # village
        self.villages = self.acquire_village_names()
        self.print_village_overview()
        self.n_villages = len(self.villages)
        self.troop_tabs = []
        self.__fill_troop_tabs()
        self.coods = {}
        self.units = ['Clubswinger', 'Scout', 'Ram', 'Chief', 'Spearman', 'Paladin', 'Catapult', 'Settler', 'Axeman', 'Teutonic Knight']
        self.__get_coordinates()
        self.hero = True if self.args.hero else False
        self.hero_village = self.args.hero_village
        self.press_alt_tab()

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
        self.goto_init()
        self.press_shift_tab(9 + self.n_villages - num)
        self.press_enter()
        self.wait(self.wait_time)
        # self.open_map()
        # self.wait(self.wait_time)
        # self.press_tab(45 + num)
        # self.press_enter()
        # self.wait(self.wait_time)

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

    def __fill_troop_tabs(self):
        file_name = 'troop_tabs.list'
        if self.args.troop_tabs:
            self.get_troop_tabs()
            f = open(file_name, 'w')
            pickle.dump(self.troop_tabs, f)
        else:
            assert os.path.exists(file_name), file_name + ' does not exist!'
            f = open(file_name, 'r')
            self.troop_tabs = pickle.load(f)

    def acquire_village_names(self):
        dic = OrderedDict()
        self.goto_init()
        self.wait()
        self.press_ctrl_and('a')
        self.press_ctrl_and('c')
        self.wait()
        self.goto_init()
        self.wait()
        self.goto_init()
        all_str = self.root.clipboard_get().encode('utf-8').split('\n')
        all_str = filter(lambda x: len(x) > 2, all_str)
        for i, val1 in enumerate(all_str):
            if val1.startswith('Villages'):
                for j, val2 in enumerate(all_str[i + 1:]):
                    if val2.startswith('Daily'):
                        break
                    if j % 2 == 0:
                        dic[val2] = {}
                        coods = ''
                        for letter in all_str[i + 1:][j + 1]:
                            try:
                                letter.decode('utf-8')
                                coods += letter
                            except UnicodeDecodeError:
                                pass
                        dic[val2]['x'] = int(coods.strip('()').split('|')[0])
                        dic[val2]['y'] = int(coods.strip('()').split('|')[1])
        return dic

    def configure_parser(self):
        self.parser.add_argument("-H", "--hero", action="store_true", help="True if hero is in village")
        self.parser.add_argument("hero_village", nargs='?', default="2", help="enter the hero village", type=int)
        self.parser.add_argument("-tt", "--troop_tabs", action="store_true", help="acquire troop tabs from travian")

    # todo get troop tabs over ctrl a
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

    # def print_troop_tabs(self):
    #     for lst, i in zip(self.troop_tabs, range(self.n_villages):
    #         print 'village ' + str(i) +

    def print_village_overview(self):
        for key, item in self.villages.iteritems():
            print '{key}:{tabs}({x}|{y})'.format(key=key, x=item['x'], y=item['y'], tabs='\t' * (2 - len(key + ':') / 8))

    @staticmethod
    def suppress_xlib_output():
        for i in range(4):
            print '\r\033[1A' + 46 * ' ',
        print '\r'


if __name__ == '__main__':
    t = Travian()
    # x.run()
