"""

This module calculates a given formula

January 2026, Skadi Wiesemann

"""

from re import fullmatch, findall
from time import sleep

from multiprocessing import Process, Manager

from faustbot.communication.Connection import Connection
from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


def eval_with_result(formel, _result_dict):
    _result_dict["eval_result"] = eval(formel)


def eval_with_mp(formel):
    manager = Manager()
    _result_dict = manager.dict()

    process = Process(target=eval_with_result, args=(formel, _result_dict))

    process.start()
    for _ in range(20):
        sleep(0.1)
        if process.is_alive():
            continue
        else:
            process.join()
            return _result_dict["eval_result"]
    process.terminate()


class MathObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".math"]

    @staticmethod
    def help():
        return ".math <Term> - Berechnet eine Formel"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".math "):
            formel = data["messageCaseSensitive"].split(" ", 1)[1]

            valid_formel_pattern = r"[0-9.(*+-/%) ]+"
            invalid_formel_pattern = r"[^0-9.(*+-/%) ]"
            if fullmatch(valid_formel_pattern, formel):
                result = eval_with_mp(formel)

                if result:
                    connection.send_back(f"Die Lösung für {formel} ist {result}", data)
                else:
                    connection.send_back(
                        "Das konnte ich nicht schnell genug für dich berechnen. :/", data
                    )

            else:
                connection.send_back(
                    f"Die Mathe-Anfrage '{formel}', sollte diese Sachen nicht enthalten: {findall(invalid_formel_pattern, formel)}",
                    data,
                )
