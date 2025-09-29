import csv

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

class ICD11Observer(PrivMsgObserverPrototype):
    with open('FaustBot/Modules/txtfiles/icd11_codes.csv') as icd11_codes:
        icd11_dict = {
            row[0]: row[1]
            for row in csv.reader(icd11_codes, delimiter=',')
        }

    @staticmethod
    def cmd():
        return ['.icd11']

    @staticmethod
    def help():
        return ['.icd11 - Gibt einen ']

    def update_on_priv_msg(self, data, connection: Connection):

        #' ' after .icd11 so that .icd11xxx doesnt trigger an IndexError at code = arr[1]
        if data['message'].startswith('.icd11 '):
            #split message
            message = data['messageCaseSensitive']
            arr = message.split(' ', 2)

            #capitalize icdCode
            code = arr[1].upper()
            print(code)

            try:
                text = self.icd11_dict.get(code).strip(' ')
            except AttributeError:
                print('Key Not Found')

            try:
                connection.send_back(f'{code} - {text}', data)
            except:
                connection.send_back(f'Fehler Versuche es erneut', data)
