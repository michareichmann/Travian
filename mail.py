#!/usr/bin/env python
__author__ = 'micha'

# ============================================
# IMPORTS
# ============================================
from smtplib import SMTP, SMTPAuthenticationError
from getpass import getpass
from email.mime.text import MIMEText
from sys import exit


# ============================================
# CLASS DEFINITION
# ============================================
class Mail:

    def __init__(self):
        self.email = 'micha.reichmann@gmail.com'
        self.message = None
        self.make_msg()
        self.username = self.email
        self.server = SMTP('smtp.gmail.com:587')
        self.init_server()

    def init_server(self):
        self.server.starttls()
        tries = 1
        while True:
            try:
                self.server.login(self.username, getpass())
                break
            except SMTPAuthenticationError:
                if tries > 2:
                    print 'too many tries! --> exiting'
                    exit(-2)
                tries += 1

    def close_connection(self):
        self.server.quit()

    def send_email(self, num=1, to=None, msg=None, subj=None):
        if to is None:
            to = self.email
        if msg is None:
            msg = self.message.as_string()
        if subj is not None:
            msg = MIMEText('')
            msg['Subject'] = subj
            msg = msg.as_string()
        for i in range(num):
            self.server.sendmail(self.email, to, msg)

    def make_msg(self, text='under attack!'):
        msg = MIMEText(text)
        msg['Subject'] = 'Travian Attack!'
        msg['From'] = self.email
        msg['To'] = self.email
        self.message = msg

    @staticmethod
    def reverse_text(text):
        rev = ''
        for letter in reversed(text):
            rev += letter
        return rev

if __name__ == '__main__':
    t = Mail()
    # t.send_email()
