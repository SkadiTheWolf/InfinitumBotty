"""

    Module to Convert one Unit to a different Unit

    February 2026, Skadi Wiesemann

"""

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

ZENT_INCH = 2.25
GRAMM_POUND = 453.592


umrechnung = {

    ('zentimeter', 'inch'): ZENT_INCH/1,
    ('inch', 'zentimeter'): ZENT_INCH,

    ('gramm', 'pound'): GRAMM_POUND/1,
    ('pound', 'gramm'): GRAMM_POUND

}

class ConvertObserver(PrivMsgObserverPrototype):

    @staticmethod
    def cmd():
        return ['.conv']

    @staticmethod
    def help():
        return '.conv <von Einheit> <zu Einheit> <Zahl> - Wandelt eine Einheit in die andere um. .conf help für eine liste von Einheiten'

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.conv') == -1 :
            return

        if data['message'].startswith('.conv'):
            print(data['message'])

            array = data['message'].split(' ') # ['.conf', 'von', 'zu', 'zahl']

            try:
                zahlString = array[3]
                von = array[1]
                zu = array[2]
            except IndexError:
                connection.send_back('Verfügbare Einheiten sind: gramm, zentimeter, pound, inch', data)
                return

            try:
                zahlString = zahlString.replace(',', '.')
                zahl = float(zahlString)
            except ValueError:
                connection.send_back('Keine Zahl', data)
                return

            faktor = umrechnung.get((von, zu))
            ergebnis = round((zahl*faktor), 2)

            connection.send_back(f'{zahlString} {von} sind {ergebnis} {zu}', data)
            return

