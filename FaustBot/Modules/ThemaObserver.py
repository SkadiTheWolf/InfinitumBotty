import random

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from essen import essen


class ThemaObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".thema"]

    @staticmethod
    def help():
        return ".thema - ein Thema aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):

        anfang = ['Gerade geht es um','Das Gespräch handelt von','Wir reden über','Das Thema ist']

        thema = ['Grönland', 'Basketball', 'Handball']

        if data['message'].startswith(".thema"):
            connection.send_back(f'{random.choice(anfang)} {random.choice(thema)}', data)




        '''if data["message"].startswith(".food"):
            connection.send_back(
                f"\001ACTION tischt {data['nick']} {random.choice(essen)} auf.\001",
                data,
            )'''
