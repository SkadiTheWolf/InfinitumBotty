from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

import random


class LetterObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".abc"]

    @staticmethod
    def help():
        return ".abc - wählt einen zufälligen Buchstaben aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".abc"):
            alphabet = "abcdefghijklmnopqrstuvwxyzäüö"

            # choose a random letter from alphabet list
            letter = random.choice(alphabet).upper()

            connection.send_back("Gewählter Buchstabe: " + letter, data)
