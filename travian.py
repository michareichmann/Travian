#!/usr/bin/env python
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


__author__ = 'micha'
# todo: print text field


# ============================================
# MAIN CLASS DEFINITION
# ============================================
class Travian(Keys, Mouse):
    def __init__(self, gui):
        Keys.__init__(self)
        Mouse.__init__(self)
        # tkinter
        self.root = gui
        # self.root.withdraw()
        # parser
        self.parser = ArgumentParser()
        self.configure_parser()
        self.args = self.parser.parse_args()
        # general stuff
        self.firefox = True
        self.msg = 'Nothing'
        self.__link_tabs = 0
        self.link_list = None
        self.wait_time = 1.5
        self.raid_wait = 0.45
        self.a = 0.1
        self.is_sitter = False
        # village
        self.villages = None
        self.read_all_str()
        self.n_villages = len(self.villages)
        self.add_stat_info()
        self.Production = self.init_production()
        # self.print_village_overview()
        # raids
        self.units = {0: 'Clubswinger', 1: 'Scout', 2: 'Ram', 3: 'Chief', 4: 'Spearman', 5: 'Paladin', 6: 'Catapult', 7: 'Settler', 8: 'Axeman', 9: 'Teutonic Knight', 10: 'Hero'}
        self.raid_info = self.get_raid_info()
        # go back to the terminal
        self.press_alt_tab()

    def run(self):
        pass

    def reset_production(self):
        self.init_production(reset=True)

    def init_production(self, reset=False):
        dic = OrderedDict()
        names = ['Lumber', 'Clay', 'Iron', 'Crop']
        for name in names:
            if reset:
                self.Production[name] = 0
            else:
                dic[name] = 0
        return dic

    # ============================================
    # region OPEN WINDOWS IN TRAVIAN
    def open_troops(self, num=0):
        self.goto_init()
        self.wait()
        self.press_tab(26)
        if num:
            self.press_ctrl_enter(num)
        else:
            self.press_enter()
            self.wait(self.wait_time)

    def close_tabs(self, num=1):
        self.goto_init()
        self.wait()
        for i in range(num):
            self.wait(self.a)
            self.press_ctrl_w()

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
        # self.press_shift_tab(16 + 2 * self.n_villages)
        # self.press_enter()
        # self.wait(1)

    def open_market(self, single=False):
        pos = self.get_mouse_position()
        self.goto_init()
        self.wait()
        self.press_shift_tab(12 + self.n_villages)
        self.press_enter()
        self.single_mode(single, pos)

    def open_offer(self):
        self.goto_init()
        self.wait()
        if 'offer' in self.link_list:
            link_tab_nr = self.link_list.index('offer')
            self.press_tab(24 + link_tab_nr)
        else:
            self.open_market()
            self.press_tab(40 + self.get_link_tabs())
        self.wait()
        self.press_enter()
        self.wait(self.wait_time)

    def change_village(self, num, single=False):
        """
        Change Village
        :param num: name of the village
        :param single: use function alone
        :return: village name
        """
        # num = self.villages.keys().index(vil) + 1
        pos = self.get_mouse_position()
        self.goto_init()
        self.wait()
        self.press_shift_tab(9 + self.n_villages - num)
        self.press_enter()
        self.single_mode(single, pos)
        return self.villages.keys()[num - 1]

    def single_mode(self, status, pos):
        if not status:
            self.wait(self.wait_time)
        else:
            self.press_alt_tab()
            self.m.move(pos[0], pos[1])

    # endregion

    # ============================================
    # region RAIDING

    def send_all_raids(self):
        # self.get_all_troop_tabs()
        for vil in range(1, self.n_villages + 1):
            self.send_raids(vil)

    def send_raids(self, village=1):
        assert len(str(village)) < 2, 'wrong village input'
        vil_name = self.villages.keys()[village - 1]
        infos = self.raid_info[vil_name]
        n_raids = len(infos['x'])
        if n_raids == 0:
            print 'no raids in infofile for', vil_name
            return
        print 'send raids for', vil_name
        # goto the village
        self.change_village(village)
        self.get_troop_tabs(vil_name)
        # open tabs and check how many raids are possible
        send_raids = []
        left_raids = self.check_raids(village, send_raids)
        # open tabs and wait
        self.open_troops(left_raids)
        # linear behaviour of the tab open time
        self.wait(left_raids * self.raid_wait + 2)
        # fill in raid info
        for raid in reversed(send_raids):
            self.wait()
            self.send_raid(village, infos['x'][raid], infos['y'][raid], infos['unit'][raid], infos['quantity'][raid], False)
            sleep(3)
            self.wait(0.5)
        # confirm and close tabs
        self.wait(self.raid_wait * left_raids + 1)
        link_tabs = self.get_link_tabs()
        for i in range(left_raids):
            self.press_tab(38 + link_tabs)
            self.press_enter()
            self.wait(self.a)
            self.press_ctrl_w()
            self.wait()

    def send_ready_tabs(self, n):
        self.goto_init()
        self.wait(1)
        self.press_tab(40 + self.get_link_tabs())
        self.wait(.05)
        self.press_enter()
        self.wait(.05)
        self.press_ctrl_w()
        self.wait(.05)
        # self.wait(0.5)
        for i in xrange(n - 1):
            self.press_enter()
            self.wait(.05)
            self.press_ctrl_w()
            self.wait(.05)

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
        :param single: mode to use functions as standalone
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
        link_tabs = self.get_link_tabs()
        self.press_tab(36 + link_tabs + n_tabs)
        self.wait()
        self.send_text(quantity)
        self.wait()
        self.press_tab(all_tabs - n_tabs)
        self.wait()
        self.send_text(x)
        self.wait()
        self.press_tab()
        self.send_text(y)
        self.wait()
        self.press_tab()
        # 1 for an attack
        self.press_down(2)
        self.press_tab()
        self.press_enter()
        if single:
            self.wait(1)
            self.press_tab(38 + link_tabs)
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

    # endregion

    # ============================================
    # region MARKETPLACE

    def send_merchant(self, vil1, vil2, lum=0, clay=0, iron=0, crop=0, go_twice=False):
        quantity = clay + lum + iron + crop
        vil1 = self.villages.keys().index(vil1) + 1
        # for i, arg in enumerate(sorted(locals().values())):
        #     if i > 1:
        #         assert type(arg) is int, '{arg} has to be of type int'.format(arg=arg)
        self.change_village(vil1)
        self.open_market()
        if not self.enough_merchants(quantity):
            return self.msg
        if self.firefox:
            self.press_tab()
            self.press_shift_tab(8)
        self.press_tab()
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
        self.send_text(vil2)
        self.wait()
        if go_twice:
            self.press_tab()
            self.wait()
            self.press_space()
            self.wait()
        self.press_enter()
        self.wait(1)
        link_tabs = self.get_link_tabs()
        print link_tabs
        self.press_tab(50 + link_tabs)
        self.press_enter()
        return 0

    def send_iron(self, vil1, vil2, iron, go_twice=False):
        self.send_merchant(vil1, vil2, iron=iron, go_twice=go_twice)

    def send_clay(self, vil1, vil2, clay, go_twice=False):
        self.send_merchant(vil1, vil2, clay=clay, go_twice=go_twice)

    def send_lumber(self, vil1, vil2, lumber, go_twice=False):
        self.send_merchant(vil1, vil2, lum=lumber, go_twice=go_twice)

    def send_crop(self, vil1, vil2, crop, go_twice=False):
        self.send_merchant(vil1, vil2, crop=crop, go_twice=go_twice)

    def market_offer(self, vil, res1, res2, quant1, quant2, num=1, max_transport=True, max_time=4, own_ally=False):

        vil_num = self.villages.keys().index(vil) + 1
        ress1 = {'Lumber': 0, 'Clay': 1, 'Iron': 2, 'Crop': 3}
        ress2 = {'Lumber': -1, 'Clay': 0, 'Iron': 1, 'Crop': 2}
        self.change_village(vil_num)
        self.open_offer()
        if not self.enough_merchants(int(quant1), int(num)):
            return
        self.press_tab()
        self.send_text(quant1)
        self.press_tab()
        self.wait()
        self.press_down(ress1[res1])
        self.press_tab()
        self.send_text(quant2)
        self.press_tab()
        self.wait()
        if ress2[res2] == -1:
            self.press_up()
        else:
            self.press_down(ress2[res2])
        if max_transport:
            self.press_tab()
            self.press_space()
            self.press_tab()
            self.send_text(max_time)
        else:
            self.press_tab(2)
        if own_ally:
            self.press_tab()
            self.press_space()
        else:
            self.press_tab()
        self.press_tab()
        self.wait()
        for i in range(num):
            self.press_enter()
            self.wait(1)
            self.press_tab()
            self.wait()

    def enough_merchants(self, quant, num=1):
        all_str = self.get_copy_all_str()
        all_str = filter(lambda x: len(x) > 2, all_str)
        n_merchants = 0
        carry_volume = 0
        for i, value in enumerate(all_str):
            if value.startswith('Merchants'):
                merchants = self.decode_utf8(value.split()[1]).split('/')
                n_merchants = int(merchants[0])
                for j, word in enumerate(all_str[i + 1].split()):
                    if word.startswith('carry'):
                        carry_volume = int(all_str[i + 1].split()[j + 1])
                break
        if not carry_volume:
            carry_volume = 1000
        # check if the division is without rest
        if (quant / float(carry_volume)).is_integer():
            required_merchants = (quant / carry_volume) * num
        else:
            required_merchants = (quant / carry_volume + 1) * num
        if required_merchants > n_merchants and quant != 200000:
            msg = 'You have not got enough merchants!'
            self.msg = msg
            print 'You have not got enough merchants!'
            return False
        else:
            return True
    # endregion

    # ============================================
    # region VILLAGE INFOS

    def read_all_str(self):
        """
        fills self.villages and __link list with information from the copied travian overview
        :return:
        """
        all_str = self.get_copy_all_str()
        all_str = filter(lambda x: len(x) > 2, all_str)
        for i, value in enumerate(all_str):
            self.acquire_village_names(all_str, i, value)
            self.acquire_link_list(all_str, i, value)

    def acquire_village_names(self, lis, index, value):
        if value.startswith('Villages'):
            dic = OrderedDict()
            for j, val2 in enumerate(lis[index + 1:]):
                if val2.startswith('Daily'):
                    break
                if j % 2 == 0:
                    vil = val2
                    dic[vil] = {}
                    coods = self.decode_utf8(lis[index + 1:][j + 1])
                    dic[vil]['x'] = int(coods.strip(' ()').split('|')[0])
                    dic[vil]['y'] = int(coods.strip(' ()').split('|')[1])
                    dic[vil]['hero'] = False
            self.villages = dic

    def acquire_link_list(self, lis, index, value):
        if value.startswith('Link list'):
            link_list = []
            count = 0
            for val in lis[index + 1:]:
                if val.startswith('Warehouse'):
                    break
                link_list.append(val.lower())
                count += 1
            self.__link_tabs = count
            self.link_list = link_list

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
        all_str = filter(lambda x: len(x) > 2, all_str)
        self.villages[vil]['troops'] = []
        for i, val1 in enumerate(all_str):
            if val1.startswith('Farm List'):
                for j, val2 in enumerate(all_str[i + 1:]):
                    if val2.startswith('Village'):
                        break
                    elif val2.startswith('Hero'):
                        self.villages[vil]['hero'] = True
                    if self.firefox:
                        if len(tabs) <= 10:
                            tabs.append(tab)
                        try:
                            num = int(val2.split('/')[1])
                            self.villages[vil]['troops'].append(num)
                            tab += 2 if num else 1
                        except (IndexError, ValueError):
                            pass
                    else:
                        if j % 2 == 0:
                            if len(tabs) <= 10:
                                tabs.append(tab)
                            try:
                                num = int(all_str[i + 1:][j + 1].strip(' /'))
                                self.villages[vil]['troops'].append(num)
                                tab += 2 if num else 1
                            except (IndexError, ValueError):
                                pass
        if self.firefox and not self.villages[vil]['hero']:
            tabs.append(tab)
        self.villages[vil]['troop tabs'] = tabs
        return tabs

    def acquire_troops_in_villages(self):
        self.open_stats()
        all_str = self.get_copy_all_str()
        all_str = filter(lambda x: len(x) > 2, all_str)
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

    def acquire_stat_info(self):
        self.open_stats()
        all_str = self.get_copy_all_str()
        found_vil = 0
        for i, val1 in enumerate(all_str):
            if found_vil == self.n_villages:
                break
            vil_name = self.villages.keys()[found_vil]
            vil = self.villages.values()[found_vil]
            next_vil = self.villages.keys()[found_vil + 1] if found_vil < self.n_villages - 1 else 'xyz'
            if val1.startswith(vil_name):
                found_vil += 1
                for k, val2 in enumerate(all_str[i + 1:]):
                    if val2.startswith(next_vil) or val2.startswith('Loyalty'):
                        break
                    info = val2.split()
                    for j, word in enumerate(info):
                        old_word = info[j - 1] if j > 0 else None
                        if word.startswith('Own'):
                            num = int(info[j - 1].strip('x'))
                            if info[j + 1].startswith('reinf'):
                                vil['reinf out'] = num
                            elif info[j + 1].startswith('attack'):
                                vil['attacks out'] = num
                        elif word.startswith('Arriving'):
                            if info[j + 1].startswith('attack'):
                                num = int(info[j - 1].strip('x'))
                                vil['attacks in'] = num
                            elif info[j + 1].startswith('reinf'):
                                num = int(info[j - 1].strip('x'))
                                vil['reinf in'] = num
                        elif word.startswith('Troops') and not old_word.startswith('attacking'):
                            num = int(info[j - 1].strip('x'))
                            vil['oasis attacks'] = num
                        elif '/' in word:
                            num = word.split('/')[0]
                            vil['merchants'] = num

    def add_stat_info(self):
        for key, value in self.villages.iteritems():
            value['attacks out'] = 0
            value['attacks in'] = 0
            value['reinf in'] = 0
            value['reinf out'] = 0
            value['merchants'] = 0
            value['oasis attacks'] = 0

    def acquire_resources(self):
        self.open_overview()
        self.wait(1)
        for i, info in enumerate(self.villages.itervalues(), 1):
            info['production'] = OrderedDict()
            self.change_village(i)
            all_text = filter(lambda x: len(x) > 2, self.get_copy_all_str())
            for j, val1 in enumerate(all_text):
                if val1.startswith('Production per hour'):
                    for k, val2 in enumerate(all_text[j + 1:]):
                        if k % 3 == 0:
                            data = [all_text[j + 1:][l] for l in xrange(k, k + 3)]
                            fac = 4 / 5. if len(data[0].split()) > 1 else 1
                            try:
                                info['production'][data[1].strip(':')] = int(fac * int(self.decode_utf8(data[2])))
                            except ValueError:
                                break

    # endregion

    # ============================================
    # region PRINT OVERVIEWS

    def get_max_vilname_length(self):
        lengths = [len(name) for name in self.villages]
        return max(lengths)

    def show_resources(self):
        self.reset_production()
        if 'production' not in self.villages.values()[0]:
            self.acquire_resources()
        l1 = self.get_max_vilname_length()
        all_length = l1 + 2 + 4
        print 'Village'.ljust(l1 + 2),
        for res in self.villages.values()[0]['production']:
            print res.rjust(len(res) + 2),
            all_length += len(res) + 2
        print
        for key, item in self.villages.iteritems():
            print key.ljust(l1 + 2),
            for name, val in item['production'].iteritems():
                self.Production[name] += val
                print str(val).rjust(len(name) + 2),
            print
        print '-' * all_length
        print ''.ljust(l1 + 2),
        for name, val in self.Production.iteritems():
            print str(val).rjust(len(name) + 2),

    def print_village_overview(self):
        for key, item in self.villages.iteritems():
            print '{key}:{tabs}({x}|{y}){hero}'.format(key=key, x=item['x'], y=item['y'], tabs=self.get_tabs(key + ':'), hero='  <--Here is your Hero' if item['hero'] else '')

    def print_raid_info(self):
        for key, item in self.raid_info.iteritems():
            print key + ':'
            for key1, item1 in item.iteritems():
                print '  {key}:{tabs}{info}'.format(key=key1, info=item1, tabs=self.get_tabs(key1 + '  :'))
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
                    print '  {unit}:{tabs}{num}'.format(unit=unit, num=num, tabs=self.get_tabs(unit + '  :'))
            print

    def print_tabs(self):
        for key, item in self.villages.iteritems():
            try:
                print '{key}:{tabs}{lst}'.format(key=key, tabs=self.get_tabs(key + ':'), lst=item['troop tabs'])
            except KeyError:
                print '{key}:{tabs}not yet checked'.format(key=key, tabs=self.get_tabs(key + ':'))

    def print_stat_info(self):
        strings = ['attacks out', 'attacks in', 'reinf in', 'reinf out', 'merchants']
        for key, village in self.villages.iteritems():
            print key + ':'
            for string in strings:
                if village[string]:
                    print '  {str}:{tabs}{val}'.format(str=string, tabs=self.get_tabs(string + ':  '), val=village[string])

    # endregion

    # ============================================
    # region MISCELLANEOUS

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
        lst = re.split('[\n\t]', self.root.clipboard_get().encode('utf-8'))
        all_str = [line.strip(' ') for line in lst]
        return all_str

    def configure_parser(self):
        self.parser.add_argument("-H", "--hero", action="store_true", help="True if hero is in village")
        self.parser.add_argument("hero_village", nargs='?', default="2", help="enter the hero village", type=int)
        self.parser.add_argument("-tt", "--troop_tabs", action="store_true", help="acquire troop tabs from travian")

    def sitter_mode(self, status):
        link_tabs = self.get_link_tabs()
        if status and not self.is_sitter and link_tabs > 0:
            self.set_link_tabs(link_tabs - 1)
            self.is_sitter = True
        if not status and self.is_sitter:
            self.set_link_tabs(link_tabs + 1)
            self.is_sitter = False
        print 'link tabs:', self.get_link_tabs()
        return self.is_sitter

    def open_previous_window(self):
        self.wait()
        self.press_alt_tab()
        return
    # endregion

    # ============================================
    # SET
    def set_link_tabs(self, value):
        self.__link_tabs = value

    # ============================================
    # GET
    def get_link_tabs(self):
        return self.__link_tabs

    @staticmethod
    def wait(sec=0.2):
        sleep(sec)

    @staticmethod
    def sort_troop_index(ind):
        """
        Sort troop list from troop window to stat window
        :param ind: troop number
        """
        return ind % 3 * 4 + ind / 3

    @staticmethod
    def get_tabs(string):
        return '\t' * (2 - len(string) / 8)

    @staticmethod
    def decode_utf8(word):
        coods = ''
        for letter in word:
            try:
                letter.decode('utf-8')
                coods += letter
            except UnicodeDecodeError:
                pass
        return coods


if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    t = Travian(root)
