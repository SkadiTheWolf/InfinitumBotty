import random

from faustbot.communication.Connection import Connection
from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from faustbot.extras.essen import essen


class GiveFoodObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".food"]

    @staticmethod
    def help():
        return ".food - gibt etwas zu essen aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".food"):
            connection.send_back(
                f"\001ACTION tischt {data['nick']} {random.choice(essen)} auf.\001",
                data,
            )
