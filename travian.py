#!/usr/bin/env python
__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from time import sleep
from keys import Keys
from mouse import Mouse
from glob import glob
from argparse import ArgumentParser
from Tkinter import Tk
# import pickle
# import os.path
from collections import OrderedDict
import re


# ============================================
# MAIN CLASS DEFINITION
# ============================================
class Travian(Keys, Mouse):
    def __init__(self):
        Keys.__init__(self)
        Mouse.__init__(self)
        # tkinter
        self.root = Tk()
        self.root.withdraw()
        # parser
        self.parser = ArgumentParser()
        self.configure_parser()
        self.args = self.parser.parse_args()
        # general stuff
        self.link_list = 5
        self.wait_time = 2
        self.a = 0.1
        # village
        self.villages = self.acquire_village_names()
        self.n_villages = len(self.villages)
        self.get_troop_tabs()
        self.print_village_overview()
        # raids
        self.units = {0: 'Clubswinger', 1: 'Scout', 2: 'Ram', 3: 'Chief', 4: 'Spearman', 5: 'Paladin', 6: 'Catapult', 7: 'Settler', 8: 'Axeman', 9: 'Teutonic Knight'}
        self.raid_info = self.get_raid_info()
        self.press_alt_tab()

    def run(self):
        pass

    # ============================================
    # OPEN WINDOWS IN TRAVIAN
    def open_troops(self, num=0):
        self.goto_init()
        self.wait()
        self.press_tab(26)
        if num:
            self.press_ctrl_enter(num)
        else:
            self.press_enter()
            self.wait(self.wait_time)

    def open_map(self):
        """
        Showing Map of the current village
        :return:
        """
        self.goto_init()
        self.wait()
        self.press_tab(4)
        self.press_enter()

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
        """
        Change Village
        :param num: number of the village
        :return: village name
        """
        self.goto_init()
        self.wait()
        self.press_shift_tab(9 + self.n_villages - num)
        self.press_enter()
        self.wait(1)
        return self.villages.keys()[num - 1]

    # ============================================
    # RAIDING
    def send_all_raids(self):
        for vil in range(1, self.n_villages + 1):
            self.send_raids(vil)

    def send_raids(self, village=1):
        assert len(str(village)) < 2, 'wrong village input'
        # get infos
        infos = self.raid_info.values()[village - 1]
        n_raids = len(infos['x'])
        if n_raids == 0:
            print 'no raids in infofile for', self.raid_info.keys()[village - 1]
            return
        print 'send raids for', self.raid_info.keys()[village - 1]
        # goto the village
        self.change_village(village)
        # open tabs
        self.open_troops(n_raids)
        self.wait(n_raids)
        # fill in raid info
        for raids in range(n_raids - 1, -1, -1):
            self.send_raid(village, infos['x'][raids], infos['y'][raids], infos['unit'][raids], infos['quantity'][raids], False)
            self.wait(0.5)
        # confirm and close tabs
        self.wait(.5 * n_raids)
        for i in range(n_raids):
            self.press_tab(43)
            self.press_enter()
            self.press_ctrl_w()
            self.wait(self.a)

    def send_raid(self, vil_num, x, y, unit_name, quantity, single=True):
        """
        send a single raid to the selected village
        :param vil_num: number of the village
        :param x: target coordinate x
        :param y: target coordinate y
        :param unit_name: unit string (first letters suffice)
        :param quantity: number of the raiding units
        :return:
        """
        if single:
            self.open_troops()
            self.change_village(vil_num)
        else:
            self.press_ctrl_tab()
        unit_num = None
        for i, unit in self.units.iteritems():
            if unit.lower().startswith(unit_name.lower()):
                unit_num = i
                break
        n_tabs = self.villages.values()[vil_num - 1]['troop tabs'][unit_num]
        all_tabs = self.villages.values()[vil_num - 1]['troop tabs'][-1] + 1
        print self.villages.keys()[vil_num - 1], n_tabs, all_tabs,
        all_tabs += 2 if self.villages.values()[vil_num - 1]['hero'] else 0
        print all_tabs
        self.press_tab(41 + n_tabs)
        self.send_text(quantity)
        self.press_tab(all_tabs - n_tabs)
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

    def get_raid_info(self):
        dic = OrderedDict()
        for name in sorted(glob('*.inf')):
            f = open(name, 'r')
            try:
                village_name = self.villages.keys()[int(name[0]) - 1]
            except (ValueError, IndexError):
                print 'wrong coordinate file:', name
            dic[village_name] = OrderedDict()
            dic[village_name]['x'] = []
            dic[village_name]['y'] = []
            dic[village_name]['unit'] = []
            dic[village_name]['unit_num'] = []
            dic[village_name]['quantity'] = []
            for line in f:
                if line.startswith('#'):
                    continue
                data = [int(x) if x[1:].isdigit() else x for x in line.split()]
                dic[village_name]['x'].append(data[0])
                dic[village_name]['y'].append(data[1])
                for i, unit in self.units.iteritems():
                    if unit.lower().startswith(data[2]):
                        dic[village_name]['unit'].append(unit)
                        dic[village_name]['unit_num'].append(i)
                        break
                dic[village_name]['quantity'].append(data[3])
        return dic

    # todo: read in troop numbers and check if you got enough to raid

    # def __fill_troop_tabs(self):
    #     file_name = 'villages.dct'
    #     if self.args.troop_tabs:
    #         self.get_troop_tabs()
    #         f = open(file_name, 'w')
    #         pickle.dump(self.villages, f)
    #     else:
    #         assert os.path.exists(file_name), file_name + ' does not exist!'
    #         f = open(file_name, 'r')
    #         self.villages = pickle.load(f)

    def acquire_village_names(self):
        dic = OrderedDict()
        all_str = self.get_copy_all_str()
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
                        dic[val2]['hero'] = False
        return dic

    def get_copy_all_str(self):
        self.goto_init()
        self.wait()
        self.press_ctrl_and('a')
        self.press_ctrl_and('c')
        self.wait()
        self.goto_init()
        self.wait()
        self.goto_init()
        # return self.root.clipboard_get().encode('utf-8').split('\n')
        return re.split('[\n\t]', self.root.clipboard_get().encode('utf-8'))

    def get_troop_tabs(self):
        self.open_troops()
        for k in range(self.n_villages):
            tabs = []
            tab = 0
            self.change_village(k + 1)
            all_str = self.get_copy_all_str()
            for i, val1 in enumerate(all_str):
                if val1.startswith('Farm List'):
                    for j, val2 in enumerate(all_str[i + 1:]):
                        if val2.startswith('Village'):
                            break
                        elif val2.startswith('Hero'):
                            self.villages.values()[k]['hero'] = True
                        if j % 2 == 0:
                            if len(tabs) <= 10:
                                tabs.append(tab)
                            try:
                                num = int(all_str[i + 1:][j + 1].strip(' /'))
                                tab = tabs[-1] + 2 if num else tabs[-1] + 1
                            except (IndexError, ValueError):
                                pass
            key = self.villages.keys()[k]
            self.villages[key]['troop tabs'] = tabs

    def configure_parser(self):
        self.parser.add_argument("-H", "--hero", action="store_true", help="True if hero is in village")
        self.parser.add_argument("hero_village", nargs='?', default="2", help="enter the hero village", type=int)
        self.parser.add_argument("-tt", "--troop_tabs", action="store_true", help="acquire troop tabs from travian")

    def print_village_overview(self):
        for key, item in self.villages.iteritems():
            print '{key}:{tabs}({x}|{y}){hero}'.format(key=key, x=item['x'], y=item['y'], tabs='\t' * (2 - len(key + ':') / 8), hero='  <--Here is your Hero' if item['hero'] else '')

    def print_raid_info(self):
        for key, item in self.raid_info.iteritems():
            print key + ':', '\n'
            for key1, item1 in item.iteritems():
                print '  {key}:{tabs}{info}'.format(key=key1, info=item1, tabs='\t' * (2 - len(key1 + '  :') / 8))

    @staticmethod
    def wait(sec=0.1):
        sleep(sec)


if __name__ == '__main__':
    t = Travian()
    # x.run()
