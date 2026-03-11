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


def decimal_to_base(base, zahl, uppercase):
    """
    Convert a decimal number to a BaseX number
    """
    out = ""
    zahl = int(zahl)
    while zahl > 0:
        digit = zahl % base
        if digit >= 10:
            digit = chr(digit + 87 - uppercase * 32)
        else:
            str(digit)
        out = f"{digit}{out}"
        zahl //= base
    return out


class BaseToBig(Exception):
    pass


class BaseObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".base"]

    @staticmethod
    def help():
        return ".base <von> <zu> <Zahl> - Rechnet eine Zahl in eine andere Base um"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".base "):
            _uppercase = data["messageCaseSensitive"].startswith(".B")

            array = data["message"].split(" ", 3)

            """
            Check every incoming number, if int go on if not return with error message 
            """

            try:
                srcBase = int(array[1])
                if srcBase > 36 or srcBase < 2:
                    connection.send_back(
                        f"von - {array[1]} ist nicht zwischen 2 und 36.", data
                    )
                    return
            except ValueError:
                connection.send_back(f"{array[1]} ist keine Ganzzahl", data)
                return

            try:
                targetBase = int(array[2])
                if targetBase > 36 or targetBase < 2:
                    connection.send_back(
                        f"zu - {array[2]} ist nicht zwischen 2 und 36.", data
                    )
                    return
            except ValueError:
                connection.send_back(f"{array[2]} ist keine Ganzzahl", data)
                return

            try:
                zahl = int(array[3], base=srcBase)
                if zahl == 0 or zahl == 1:
                    connection.send_back(f"Das schaffst du ohne mich :)", data)
                    return
            except ValueError:
                connection.send_back(
                    f"{array[3]} ist keine valide Zahl mit Base {srcBase}", data
                )
                return

            """
            return 0 if either number is 0
            """

            if srcBase != 10 and targetBase != 10:
                decimal_note = f" ({zahl} in Dezimal)"
            else:
                decimal_note = ""

            connection.send_back(
                f"Die Zahl {decimal_to_base(zahl=zahl, base=srcBase, uppercase=_uppercase)} zur Basis {srcBase} entspricht {decimal_to_base(zahl=zahl, base=targetBase, uppercase=_uppercase)} zur Basis {targetBase}{decimal_note}.",
                data,
            )
            return
