from random import choice

class Themen(list):
    def __init__(self):
        with open("faustbot/modules/txtfiles/themen.txt") as txt:
            super().__init__(line.strip() for line in txt.readlines())
    def reload(self):
        self.__init__()
    def get_random(self):
        return choice(self)

