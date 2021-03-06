__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from pymouse import PyMouse


# ============================================
# CLASS DEFINITION
# ============================================
class Mouse:

    def __init__(self):
        self.m = PyMouse()
        self.suppress_xlib_output(2)

    def goto_init(self):
        self.m.click(65, 148)

    def get_mouse_position(self):
        return self.m.position()

    @staticmethod
    def suppress_xlib_output(num):
        for i in range(num):
            print '\r\033[1A' + 46 * ' ',
        print
