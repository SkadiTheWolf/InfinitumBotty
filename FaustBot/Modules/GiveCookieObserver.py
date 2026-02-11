import random

from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

class GiveCookieObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".cookie"]

    @staticmethod
    def help():
        return ".cookie - verteilt Kekse; oder auch nicht"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".cookie"):

            with open("FaustBot/Modules/txtfiles/kekse.txt") as kekse:
                keks = random.choice(kekse.readlines())
                kekse.close()

            connection.send_back(
                f"\001ACTION schenkt {data['nick']} {keks}.\001", data
            )
