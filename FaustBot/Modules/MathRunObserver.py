from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from random import randrange
from time import sleep


class MathRunObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".s", ".startmath", ".stopmath"]

    @staticmethod
    def help():
        return '".startmath" startet eine Reihe von Aufgaben. ".stopmath" beendet sie. Lösungen mit ".s Lösung" eingeben.'

    def __init__(self):
        super().__init__()
        self.players = {}
        self.solutionForGame = 0
        self.type = 0
        self.running = False
        self.oldSolution = 0

    def update_on_priv_msg(self, data, connection: Connection):
        if (
            data["message"].startswith(".s ")
            and not data["message"].startswith(".startmath")
            and not data["message"].startswith(".stopmath")
        ):
            self.solution(data, connection)
        if data["message"].startswith(".startmath"):
            self.start_math(data, connection)
        if data["message"].startswith(".stopmath"):
            self.stop_math(data, connection)

    def solution(self, data, connection):
        nick = data["nick"]
        solutionByPlayer = data["message"].split()[1]
        if solutionByPlayer is None:
            connection.send_back("Du hast keine Lösung angegeben " + nick, data)
            return
        if solutionByPlayer == str(self.solutionForGame):
            connection.send_channel("Korrekte Lösung " + nick)
            if nick not in self.players:
                self.players[nick] = 0
            self.players[nick] += 1
            self.oldSolution = self.solutionForGame
            self.start_math(data, connection)
            return
        if solutionByPlayer == str(self.oldSolution):
            connection.send_channel("Korrekte Lösung für das Problem davor " + nick)
            if nick not in self.players:
                self.players[nick] = 0
            self.players[nick] += 1
            return
        connection.send_channel("Sorry die Lösung ist falsch " + nick)

    def start_math(self, data, connection):
        if "easy" in data["message"]:
            summand1 = randrange(1, 100)
            summand2 = randrange(1, 11)
            operation = randrange(1, 3)
        else:
            summand1 = randrange(10, 200)
            summand2 = randrange(5, 51)
            operation = randrange(1, 5)
        if operation == 1:
            self.solutionForGame = summand1 - summand2
            connection.send_channel(f"{str(summand1)} - {str(summand2)} = ?")
        if operation == 2:
            self.solutionForGame = summand1 + summand2
            connection.send_channel(f"{str(summand1)} + {str(summand2)} = ?")
        if operation == 3:
            summand1 = randrange(11, 40)
            self.solutionForGame = summand1 * summand2
            connection.send_channel(f"{str(summand1)} * {str(summand2)} = ?")
        if operation == 4:
            summand1 = randrange(110, 400)
            self.solutionForGame = summand1 // summand2
            summand1 = summand2 * self.solutionForGame
            connection.send_channel(f"{str(summand1)} / {str(summand2)} = ?")

        if not self.running:
            self.running = True
            self.stop_Timer(data, connection)

    def stop_math(self, data, connection):
        for player in self.players.keys():
            if self.players[player] == 1:
                connection.send_channel(
                    f"{player} hat {str(self.players[player])} Punkt."
                )
            else:
                connection.send_channel(
                    f"{player} hat {str(self.players[player])} Punkte."
                )
        connection.send_channel("Mathrun beendet")
        self.players = {}
        self.solutionForGame = 0
        self.type = 0
        self.running = False

    def stop_Timer(self, data, connection):
        sleep(120)
        if self.running:
            self.stop_math(data, connection)
