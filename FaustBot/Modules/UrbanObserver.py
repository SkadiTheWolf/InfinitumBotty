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

        if data['message'].find('.urban') == -1:
            return

        #split incoming message in '.urban' and '<term>'
        message = data['message'].split(' ', 1)

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





        '''w = wikipedia.set_lang('de')
        q = data['message'].split(' ')
        query = ''
        for word in q:
            if word.strip() != '.w':
                query += word + ' '
        w = wikipedia.search(query)
        if w.__len__() == 0:
            connection.send_back(data['nick'] + ', ' +
                                'ich habe dazu keinen eintrag gefunden!',
                                 data)
            return
        try:
            page = wikipedia.WikipediaPage(w.pop(0))
        except wikipedia.DisambiguationError as error:
            print('disambiguation page')
            page = wikipedia.WikipediaPage(error.args[1][0])
        connection.send_back(data['nick'] + ' ' + page.url, data)
        index = 51 + page.summary[50:350].rfind('. ')
        if index == 50 or index > 230:
            index = page.summary[0:350].rfind(' ')
            connection.send_back(page.summary[0:index], data)
        else:
            connection.send_back(page.summary[0:index], data)'''