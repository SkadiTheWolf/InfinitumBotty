from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
import requests

class UrbanObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".urban"]

    @staticmethod
    def help():
        return ".urban <term> - fragt Urban Dictionary zu <term> ab"

    def update_on_priv_msg(self, data, connection):
        if data['message'].find('.urban') == -1:
            return

        if data['message'].startswith('.urban'):

            arr = data['message'].split(' ',1)

            if arr[0] == ".urban":
                search = arr[1]

                contents = requests.get(
                    f'https://unofficialurbandictionaryapi.com/api/search?term={search}&limit=1&page=1&')

                contentStr = str(contents.content)
                status = int(contents.status_code)
                # print(contentStr)
                # print(status)

                if status == 200:

                    indexWord = contentStr.index('"word"')
                    indexWordEnd = contentStr.index('","meaning"')
                    indexMeaning = contentStr.index('"meaning"')
                    indexMeaningEnd = contentStr.index('","example"')

                    WordStr = contentStr[indexWord:indexWordEnd]
                    MeaningStr = contentStr[indexMeaning:indexMeaningEnd]
                    WordSplit = WordStr.split('":"')
                    MeaningSplit = MeaningStr.split('":"')

                    connection.send_back(self, f'Wort: {WordSplit}')
                    connection.send_back(self, f'Meaning: {MeaningSplit}')






