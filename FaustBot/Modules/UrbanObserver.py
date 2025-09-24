import requests

from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class UrbanObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".urban"]

    @staticmethod
    def help():
        return ".urban <term> - fragt Urban Dictionary zu <term> ab"

    def update_on_priv_msg(self, data, connection):

        if data['messageCaseSensitive'].find('.urban') == -1:
            return

        #split incoming message in '.urban' and '<term>'
        message = data['messageCaseSensitive'].split(' ', 1)

        #request content from Urban Dict with <term>
        search = message[1]
        contents = requests.get(f'https://unofficialurbandictionaryapi.com/api/search?term={search}&limit=1&page=1&')

        #use build in tools to extract content and status code for further processing
        contentStr = str(contents.content)
        status = int(contents.status_code)

        if status == 200:

            #determin beginning and end of searched word and description
            indexWord = contentStr.index('"word"')
            indexWordEnd = contentStr.index('","meaning"')
            indexMeaning = contentStr.index('"meaning"')
            indexMeaningEnd = contentStr.index('","example"')

            #extracting content
            WordStr = contentStr[indexWord:indexWordEnd]
            MeaningStr = contentStr[indexMeaning:indexMeaningEnd]
            MeaningStr = MeaningStr.replace('\\n', ' ').replace('\\', '')
            WordSplit = WordStr.split('":"')
            MeaningSplit = MeaningStr.split('":"')

            connection.send_back(f'{data['nick']} Das gesuchte Wort {WordSplit[1]} hat folgende Bedeutung:',data)
            connection.send_back(MeaningSplit[1], data)


        else:
            connection.send_back(f'Ich konnte leider keine definition für {message[1]} finden', data)