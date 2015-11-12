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
from collections import OrderedDict
import re


# todo: GUI
# todo: Alarmchecker

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
        self.print_village_overview()
        # raids
        self.units = {0: 'Clubswinger', 1: 'Scout', 2: 'Ram', 3: 'Chief', 4: 'Spearman', 5: 'Paladin', 6: 'Catapult', 7: 'Settler', 8: 'Axeman', 9: 'Teutonic Knight', 10: 'Hero'}
        self.raid_info = self.get_raid_info()
        # go back to the terminal
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

    def open_stats(self):
        """
        Maneuver to Village Statistics in Travian
        """
        self.goto_init()
        self.wait()
        self.press_shift_tab(9 + self.n_villages)
        self.press_enter()
        self.wait(self.wait_time)
        self.press_shift_tab(16 + 2 * self.n_villages)
        self.press_enter()
        self.wait(1)

    def open_market(self):
        self.goto_init()
        self.wait()
        self.press_shift_tab(12 + self.n_villages)
        self.press_enter()
        self.wait(self.wait_time)

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
        self.get_all_troop_tabs()
        for vil in range(1, self.n_villages + 1):
            self.send_raids(vil, False)

    def send_raids(self, village=1, single=True):
        assert len(str(village)) < 2, 'wrong village input'
        vil_name = self.villages.keys()[village - 1]
        # get troop tabs
        if single:
            self.get_troop_tabs(vil_name)
        # get infos
        infos = self.raid_info[vil_name]
        # troops = self.villages.values()[village - 1]['troops']
        n_raids = len(infos['x'])
        if n_raids == 0:
            print 'no raids in infofile for', self.raid_info.keys()[village - 1]
            return
        print 'send raids for', self.raid_info.keys()[village - 1]
        # goto the village
        self.change_village(village)
        # open tabs and check how many raids are possible
        send_raids = []
        left_raids = self.check_raids(village, send_raids)
        self.open_troops(left_raids)
        self.wait(left_raids * 0.6)
        # fill in raid info
        for raid in reversed(send_raids):
            self.send_raid(village, infos['x'][raid], infos['y'][raid], infos['unit'][raid], infos['quantity'][raid], False)
            self.wait(0.5)
        # confirm and close tabs
        self.wait(.4 * n_raids)
        for i in range(left_raids):
            self.press_tab(43)
            self.press_enter()
            self.wait(self.a)
            self.press_ctrl_w()
            self.wait()

    def check_raids(self, village, send_raids=None):
        village -= 1
        infos = self.raid_info.values()[village]
        troops = self.villages.values()[village]['troops']
        left_raids = 0
        all_raids = len(infos['x'])
        send_raids = [] if send_raids is None else send_raids
        sent_troops = [0 * x for x in range(10)]
        for raid in range(all_raids):
            if self.__check_raid(raid, sent_troops, infos, troops):
                left_raids += 1
                send_raids.append(raid)
        print 'sent troops:', sent_troops
        print send_raids
        return left_raids

    @staticmethod
    def __check_raid(raid, sent_troops, infos, troops):
        unit_num = infos['unit_num'][raid]
        print raid, infos['unit'][raid], troops[unit_num], sent_troops[unit_num], infos['quantity'][raid]
        if not troops[unit_num] - sent_troops[unit_num] < infos['quantity'][raid]:
            sent_troops[unit_num] += infos['quantity'][raid]
            return True
        else:
            return False

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
        all_tabs += 2 if self.villages.values()[vil_num - 1]['hero'] else 0
        self.press_tab(41 + n_tabs)
        self.send_text(quantity)
        self.press_tab(all_tabs - n_tabs)
        self.send_text(x)
        self.press_tab()
        self.send_text(y)
        self.press_tab()
        # 1 for an attack
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
            # dic[village_name]['troops'] = [0 * x for x in range(10)]
            for line in f:
                if line.startswith('#'):
                    continue
                data = [int(x) if x[-1].isdigit() else x for x in line.split()]
                dic[village_name]['x'].append(data[0])
                dic[village_name]['y'].append(data[1])
                for i, unit in self.units.iteritems():
                    if unit.lower().startswith(data[2]):
                        dic[village_name]['unit'].append(unit)
                        dic[village_name]['unit_num'].append(i)
                        # dic[village_name]['troops'][i] += data[3]
                        break
                dic[village_name]['quantity'].append(data[3])

        return dic

    # ============================================
    # MARKETPLACE
    def send_merchant(self, vil1, vil2, lum, clay, iron, crop, go_twice=False):
        vil2 -= 1
        for i, arg in enumerate(sorted(locals().values())):
            if i > 1:
                assert type(arg) is int, '{arg} has to be of type int'.format(arg=arg)
        self.change_village(vil1)
        self.open_market()
        self.send_text(lum)
        self.wait()
        self.press_tab()
        self.send_text(clay)
        self.wait()
        self.press_tab()
        self.send_text(iron)
        self.wait()
        self.press_tab()
        self.send_text(crop)
        self.wait()
        self.press_tab()
        self.send_text(self.villages.keys()[vil2])
        self.wait()
        if go_twice:
            self.press_tab()
            self.press_space()
            self.wait()
        self.press_enter()
        self.wait(1)
        self.press_tab(55)
        self.press_enter()

    # ============================================
    # VILLAGE INFOS
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

    def get_all_troop_tabs(self, skip_empty=True):
        self.open_troops()
        for village in self.villages:
            # skip this if there is no raid to send
            if skip_empty and len(self.raid_info[village]['x']) == 0:
                continue
            self.get_troop_tabs(village, False)

    def get_troop_tabs(self, vil, single=True):
        if single:
            self.open_troops()
        vil_num = self.villages.keys().index(vil) + 1
        tabs = []
        tab = 0
        self.change_village(vil_num)
        all_str = self.get_copy_all_str()
        self.villages[vil]['troops'] = []
        for i, val1 in enumerate(all_str):
            if val1.startswith('Farm List'):
                for j, val2 in enumerate(all_str[i + 1:]):
                    if val2.startswith('Village'):
                        break
                    elif val2.startswith('Hero'):
                        self.villages[vil]['hero'] = True
                    if j % 2 == 0:
                        if len(tabs) <= 10:
                            tabs.append(tab)
                        try:
                            num = int(all_str[i + 1:][j + 1].strip(' /'))
                            self.villages[vil]['troops'].append(num)
                            tab += 2 if num else 1
                        except (IndexError, ValueError):
                            pass
        self.villages[vil]['troop tabs'] = tabs

    def acquire_troops_in_villages(self):
        self.open_stats()
        all_str = self.get_copy_all_str()
        vil = 0
        for i, val1 in enumerate(all_str):
                if val1.startswith('Troops in villages'):
                    for j, val2 in enumerate(all_str[i + 1:]):
                        troops = [0] * 11
                        if val2.startswith('Troops'):
                            for k, val3 in zip(range(11), all_str[j + i + 2:]):
                                troops[self.sort_troop_index(k)] = int(val3)
                            key = self.villages.keys()[vil]
                            self.villages[key]['troops'] = troops
                            vil += 1

    # ============================================
    # PRINT OVERVIEWS
    def print_village_overview(self):
        for key, item in self.villages.iteritems():
            print '{key}:{tabs}({x}|{y}){hero}'.format(key=key, x=item['x'], y=item['y'], tabs='\t' * (2 - len(key + ':') / 8), hero='  <--Here is your Hero' if item['hero'] else '')

    def print_raid_info(self):
        for key, item in self.raid_info.iteritems():
            print key + ':'
            for key1, item1 in item.iteritems():
                print '  {key}:{tabs}{info}'.format(key=key1, info=item1, tabs='\t' * (2 - len(key1 + '  :') / 8))
            print

    def print_troops(self):
        for key, item in self.villages.iteritems():
            print key + ':'
            if 'troops' not in item.keys():
                print '  not checked'
                continue
            for i, num in enumerate(item['troops']):
                unit = 'Teutons' if self.units[i].startswith('Teut') else self.units[i]
                if num:
                    print '  {unit}:{tabs}{num}'.format(unit=unit, num=num, tabs='\t' * (2 - len(unit + '  :') / 8))
            print

    def print_tabs(self):
        for key, item in self.villages.iteritems():
            try:
                print '{key}:{tabs}{lst}'.format(key=key, tabs='\t' * (2 - len(key + ':') / 8), lst=item['troop tabs'])
            except KeyError:
                print '{key}:{tabs}not yet checked'.format(key=key, tabs='\t' * (2 - len(key + ':') / 8))

    # ============================================
    # MISCELLANEOUS
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

    @staticmethod
    def wait(sec=0.1):
        sleep(sec)

    @staticmethod
    def sort_troop_index(ind):
        """
        Sort troop list from troop window to stat window
        :param ind: troop number
        """
        return ind % 3 * 4 + ind / 3

    def configure_parser(self):
        self.parser.add_argument("-H", "--hero", action="store_true", help="True if hero is in village")
        self.parser.add_argument("hero_village", nargs='?', default="2", help="enter the hero village", type=int)
        self.parser.add_argument("-tt", "--troop_tabs", action="store_true", help="acquire troop tabs from travian")

if __name__ == '__main__':
    t = Travian()
    # x.run()
