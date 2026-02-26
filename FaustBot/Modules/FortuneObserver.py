"""

This module ouputs a random quote

September 2025, Skadi Wiesemann

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


class FortuneObserver(PrivMsgObserverPrototype):

    @staticmethod
    def cmd():
        return ['.fortune']

    @staticmethod
    def help():
        return ['.fortune - Gibt ein zufälliges Zitat aus']

    def update_on_priv_msg(self, data, connection: Connection):

        #' ' after .icd11 so that .icd11xxx doesnt trigger an IndexError at code = arr[1]
        if data['message'].startswith('.fortune'):

            out = get_quote()
            print(len(out))

            while len(out) > 400:
                out = get_quote()
                print(len(out))

            connection.send_back(out, data)
            return


