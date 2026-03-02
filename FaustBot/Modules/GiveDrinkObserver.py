import random

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class GiveDrinkObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".drink"]

    @staticmethod
    def help():
        return ".drink - schenkt Getränke aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".drink"):

            with open("FaustBot/Modules/txtfiles/getraenke.txt") as getraenke:
                getraenk = random.choice(getraenke.readlines())
                getraenke.close()

            connection.send_back(
                f"\001ACTION schenkt {data.get('nick')} {getraenk} ein.\001",
                data,
            )
