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


def fehler(data, connection: Connection, *args):
    if len(args) != 0:
        connection.send_back(f"Fehler: {args[0]}", data)
    else:
        connection.send_back('Fehler', data)


class MathObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".math"]

    @staticmethod
    def help():
        return ".math <Term> - Berechnet eine Formel"

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].startswith('.math'):

            # Vorbereitung
            ausdruck = data['message'].split(' ', -1)

            if len(ausdruck) == 4:
                # eg .math log 10 10
                #      0    1   2  3
                print(ausdruck)
                if ausdruck[1] == "log":
                    try:
                        loesung = math.log(float(ausdruck[2]), float(ausdruck[3]))
                    except ValueError:
                        fehler(data, connection, "ValueError")
                        return
                    except ZeroDivisionError:
                        fehler(data, connection, "ZeroDivisionError")
                        return
                elif ausdruck[1] == "pow":
                    try:
                        loesung = math.pow(float(ausdruck[2]), float(ausdruck[3]))
                    except ValueError:
                        fehler(data, connection, "ValueError")
                        return

                else:
                    if check_if_int(ausdruck[1]) is not ValueError:
                        a = int(ausdruck[1])
                    else:
                        fehler(data, connection, "ValueError")
                        return

                    if check_if_operand(ausdruck[2]):
                        operand = ausdruck[2]
                    else:
                        fehler(data, connection, "Kein Operand")
                        return

                    if check_if_int(ausdruck[3]) is not ValueError:
                        b = int(ausdruck[3])
                    else:
                        fehler(data, connection, "ValueError")
                        return

            elif len(ausdruck) == 2:
                # Vorbereitung 2
                operands = ["+", "-", "*", "/"]
                ausdruckWithoutSpace = [*ausdruck[1]]
                if check_if_int(ausdruckWithoutSpace[0]) is not ValueError:
                    a = int(ausdruckWithoutSpace[0])
                else:
                    fehler(data, connection, "ValueError")
                    return

                if check_if_operand(ausdruckWithoutSpace[1]):
                    operand = ausdruckWithoutSpace[1]
                else:
                    fehler(data, connection, "Kein Operand")
                    return

                if check_if_int(ausdruckWithoutSpace[2]) is not ValueError:
                    b = int(ausdruckWithoutSpace[2])
                else:
                    fehler(data, connection, "ValueError")
                    return

            elif len(ausdruck) == 3:
                # Vorbereitung 3
                ausdruckCommand = ausdruck[1]
                try:
                    a  = int(ausdruck[2])
                except ValueError:
                    try:
                        a = float(ausdruck[2])
                    except ValueError:
                        fehler(data, connection, "ValueError")
                        return

                if isinstance(a, int):
                    if ausdruckCommand == "fact":
                        loesung = math.factorial(a)

                elif isinstance(a, float) or isinstance(a, int):
                    if ausdruckCommand == "sqrt":
                        loesung = math.sqrt(a)

                    elif ausdruckCommand == "log":
                        loesung = math.log(a)



            else:
                fehler(data, connection)
                return
            if "operand" in vars():
                # Addition
                if operand == "+":
                    loesung = a + b

                elif operand == "-":
                    loesung = a - b

                elif operand == "*":
                    loesung = a * b

                elif operand == "/":
                    try:
                        loesung = a / b
                    except ZeroDivisionError:
                        fehler(data, connection, "ZeroDivisionError")

                else:
                    fehler(data, connection)
                    return

            try:
                connection.send_back(loesung, data)
                return
            except UnboundLocalError:
                fehler(data, connection, "UnbountLocal loesung")
                return
            except ValueError:
                fehler(data, connection, "Zahl Zu Gross")

