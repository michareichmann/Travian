__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from pykeyboard import PyKeyboard

class Keys:

    def __init__(self):
        self.k = PyKeyboard()

    def press_tab(self, num=1):
        for i in range(num):
            self.k.tap_key(self.k.tab_key)

    def press_enter(self):
        self.k.tap_key(self.k.enter_key)

    def press_down(self, num=1):
        for i in range(num):
            self.k.tap_key(self.k.down_key)

    def send_text(self, text):
        text = str(text)
        for letter in text:
            self.k.tap_key(letter)

    def press_ctrl_enter(self, num=1):
        for i in range(num):
            self.k.press_key(self.k.control_key)
            self.press_enter()
            self.k.release_key(self.k.control_key)

    def press_ctrl_tab(self, num=1):
        for i in range(num):
            self.k.press_key(self.k.control_key)
            self.press_tab()
            self.k.release_key(self.k.control_key)

    def press_ctrl_w(self, num=1):
        for i in range(num):
            self.k.press_key(self.k.control_key)
            self.k.tap_key('w')
            self.k.release_key(self.k.control_key)

    def press_shift_left(self, num=1):
        for i in range(num):
            self.k.press_key(self.k.shift_key)
            self.k.tap_key(self.k.left_key)
            self.k.release_key(self.k.shift_key)

    def press_ctrl_and(self, letter, num=1):
        assert type(letter) is str, 'The letter has to be a string'
        for i in range(num):
            self.k.press_key(self.k.control_key)
            self.k.tap_key(letter)
            self.k.release_key(self.k.control_key)