import random
from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class ThemaObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".thema"]

    @staticmethod
    def help():
        return ".thema - gibt ein Thema aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].startswith(".thema"):

            anfang = ['Gerade geht es um','Das Gespräch handelt von','Wir reden über','Das Thema ist']

            with open('FaustBot/Modules/txtfiles/themen.txt') as themen:
                thema = random.choice(themen.readlines())
                themen.close()

            connection.send_back(f'{random.choice(anfang)} {thema}', data)


