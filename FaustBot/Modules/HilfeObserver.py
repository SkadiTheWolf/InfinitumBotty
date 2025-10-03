"""

This module prints some resources for distressed and suicidal People

September 2025 Skadi Wiesemann

"""

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

class HilfeObserver(PrivMsgObserverPrototype):

    @staticmethod
    def cmd():
        return ['.hilfe']

    @staticmethod
    def help():
        return ['.hilfe - Gibt anlaufstellen für Akute Hilfe aus']

    def update_on_priv_msg(self, data, connection: Connection):

        if data['message'].startswith('.hilfe'):

            connection.send_back('Wir sind keine ausgebildteten Therapeuten. Bitte wende dich in akuten Fällen von Suizidalität oder psychologischen Ausnahmezuständen an folgende Orte:', data)
            connection.send_back('Rettungsdienst: Tel: 112', data)
            connection.send_back('Telefonseelsorge: https://telefonseelsorge.de', data)
            connection.send_back('Für Kinder und Eltern: https://nummergegenkummer.de, https://dajeb.de', data)
            connection.send_back('Hilfe bei Gewalt und Straftaten: https://weisser-ring.de/', data)
