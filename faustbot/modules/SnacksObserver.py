import random

from faustbot.communication.Connection import Connection
from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from faustbot.extras.snacks import snacks


class SnacksObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".snack"]

    @staticmethod
    def help():
        return ".snack - teilt Snacks aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".snack"):
            connection.send_back(
                f"\001ACTION serviert {data['nick']} {random.choice(snacks)}.\001", data
            )
