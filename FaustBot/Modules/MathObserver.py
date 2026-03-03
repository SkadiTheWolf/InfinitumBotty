"""

This module takes an expression and calculates the result

March 2026, Skadi Wiesemann

"""
import math

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.BaseObserver import check_if_int
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

def check_if_operand(operand):
    if operand not in ['+', '-', '*', '/']:
        return False
    else:
        return True


def fehler(data, connection: Connection):
    connection.send_back('Fehler', data)


class MathObserver(PrivMsgObserverPrototype):

    @staticmethod
    def cmd():
        return ['.math']

    @staticmethod
    def help():
        return '.math - Berechnet einen Mathematischen Ausdruck'

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].startswith('.math'):

            # Vorbereitung
            ausdruck = data['message'].split(' ', -1)

            if check_if_int(ausdruck[1]) is not ValueError:
                a = ausdruck[1]
            else:
                fehler(data, connection)
                return

            if check_if_operand(ausdruck[2]):
                operand = ausdruck[2]
            else:
                fehler(data, connection)
                return

            if check_if_int(ausdruck[3]) is not ValueError:
                b = ausdruck[3]
            else:
                fehler(data, connection)
                return

            # Addition
            if operand == "+":
                loesung = a + b
                connection.send_back(loesung, data)


            return
