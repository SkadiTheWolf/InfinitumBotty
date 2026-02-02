"""

This module calculates a decimal to binary and back

January 2026, Skadi Wiesemann

"""

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


def check_if_int(zahl):
    """
    Checking if the different inputs are an Integer
    """
    try:
        int(zahl)
    except ValueError:
        return ValueError


def check_if_base(base, zahl):
    """
    Checking if the Number entered is a BaseX number by taking the different digits and comparing it to X-1
    """
    while zahl != 0:
        digit = zahl % 10
        if digit >= base:
            return False
        zahl //= 10
    return True


def check_if_bigger(von, zu):
    """
    Check wich Base is bigger
    """
    if von > zu:
        return True
    else:
        return False


def decimal_to_base(base, zahl):
    out = ''
    zahl = int(zahl)
    while zahl > 0:

        out = str(zahl% base) + out
        zahl //= base
    return out


def base_to_decimal(base, zahl):

    digit, position = 0, 0
    while zahl:
        digit += (zahl % 10) * (base ** position)
        zahl //= 10
        position += 1
    out = str(digit)
    return out


def base_to_base(von, zu, zahl):

    out = decimal_to_base(zu, base_to_decimal(von, zahl))

    return out


class BaseObserver(PrivMsgObserverPrototype):

    @staticmethod
    def cmd():
        return ['.base']

    @staticmethod
    def help():
        return ".base <von> <zu> <Zahl> - Rechnet eine Zahl in eine andere Base um"

    def update_on_priv_msg(self, data: dict, connection: Connection):

        if data['message'].startswith('.base'):

            array = data['message'].split(' ', 3)

            zahlString = array[3]
            err = check_if_int(zahlString)
            if err == ValueError:
                connection.send_back(f'{zahlString} ist keine Ganzzahl', data)
                return
            zahl = int(zahlString)

            vonString = array[1]
            err = check_if_int(vonString)
            if err == ValueError:
                connection.send_back(f'{vonString} ist keine Ganzzahl', data)
                return
            von = int(vonString)

            zuString = array[2]
            err = check_if_int(zuString)
            if err == ValueError:
                connection.send_back(f'{zuString} ist keine Ganzzahl', data)
                return
            zu = int(zuString)

            bigger = check_if_bigger(von, zu)

            isBase = check_if_base(von, zahl)

            if von == 0 or zu == 0 or zahl == 0:
                connection.send_back(f'Die {zahlString} in Base{zuString} ist 0', data)
                return

            if von > 32 or zu > 32:
                connection.send_back('Zahlen zu groß', data)
                return

            if not isBase:
                connection.send_back(f'Die Zahl {zahlString} ist keine Base{vonString} Zahl', data)
                return

            if zahl > 1000000:
                connection.send_back(f'Zahl zu Groß', data)
                return

            out = ''
            if zu == 10:
                out = base_to_decimal(von, zahl)

            elif von == 10:
                out = decimal_to_base(zu, zahl)

            elif bigger:
                out = base_to_base(von, zu, zahl)

            elif not bigger:
                out = base_to_base(von, zu, zahl)

            else:
                connection.send_back('Unbekannter Fehler', data)

            connection.send_back(f'Die Zahl {zahlString} entspricht {out}', data)
