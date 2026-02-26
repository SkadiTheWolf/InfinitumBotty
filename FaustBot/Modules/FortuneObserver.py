"""

This module ouputs a random quote

February 2026, Skadi Wiesemann

"""


import random
import os

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

def get_quote():
    file = random.choice(os.listdir('FaustBot/Modules/txtfiles/zitate'))

    with open(f'FaustBot/Modules/txtfiles/zitate/{file}', 'r') as f:
        zitate = f.read()
    f.close()

    arr_zitate = zitate.split('%')
    out = ""
    for zitat in random.sample(arr_zitate, k=1):
        out = zitat.replace('\n', ' ')

    return out

def check_for_bad(out):
    with open('FaustBot/Modules/txtfiles/badquotes.txt', 'rt') as file:
        badquotes = file.read()
        for zitat in badquotes.split('\n'):
            if out == zitat:
                return True
            else:
                continue
        file.close()
        return False

class FortuneObserver(PrivMsgObserverPrototype):

    @staticmethod
    def cmd():
        return ['.fortune']

    @staticmethod
    def help():
        return ['.fortune - Gibt ein zufälliges Zitat aus. .bad setzt das Zitat auf eine Blacklist']

    def update_on_priv_msg(self, data, connection: Connection):

        global lastQuote

        if data['message'].startswith('.fortune'):

            out = get_quote()
            badquote = check_for_bad(out)

            while len(out) > 400:
                while badquote:
                    out = get_quote()

            connection.send_back(out, data)

            lastQuote = out

            return

        if data['message'].startswith('.bad'):
            with open('FaustBot/Modules/txtfiles/badquotes.txt', 'at') as f:
                f.write(f'{lastQuote}\n')
            f.close()

