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