"""

This module calculates a given formula

January 2026, Skadi Wiesemann

"""
import subprocess

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

class MathObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".math"]

    @staticmethod
    def help():
        return ".math <Term> - Berechnet eine Formel"

    def update_on_priv_msg(self, data: dict, connection: Connection):

        if data['message'].startswith(".math"):

            formel = data['messageCaseSensitive'].split(' ', 1)

            try:
                lösung = ''
                lösung = subprocess.run(['python', 'FaustBot/Modules/MathSupplementary.py'],capture_output=True, text=True, input=formel[1], timeout=2)
                connection.send_back(f'Die Lösung für {formel[1]} ist {lösung.stdout}', data)

            except subprocess.TimeoutExpired:
                connection.send_back('Fehler: Timeout', data)
