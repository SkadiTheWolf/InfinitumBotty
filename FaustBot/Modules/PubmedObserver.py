import requests

from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class PubmedObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".pubmed"]

    @staticmethod
    def help():
        return (".pubmed <term> - fragt Pub Med zu <term> ab")

    def update_on_priv_msg(self, data, connection):

        if data['messageCaseSensitive'].find('.pubmed') == -1:
            return

        #split incoming message in '.urban' and '<term>'
        message = data['messageCaseSensitive'].split(' ', 1)

        #request ids from Pubmed with <term>
        search = message[1]
        contents = requests.get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={search}')

        #use build in tools to extract content and status code for further processing
        contentStr = str(contents.content)
        status = int(contents.status_code)


        replaced = contentStr.replace('<Id>', '').replace('</Id>\\n', ' ').replace('<IdList>\\n', " ")  #
        split = replaced.split(" ")
        onlyFive = split[10:13]

        if status == 200:
            for indices in onlyFive:
                try:
                    IdContents = requests.get(
                        f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={indices}&version=2.0')
                    IdContentsStr = str(IdContents.content)
                    Title = IdContentsStr.replace('<Title>', '~').replace('</Title>', '~')
                    TitleArr = Title.split('~')
                    connection.send_back(TitleArr[1],data)

                    doi = IdContentsStr.replace('<ELocationID>', "~").replace('</ELocationID>', '~')
                    doiArr = doi.split('~')
                    connection.send_back(doiArr[1],data)
                    connection.send_back(f'https://pubmed.ncbi.nlm.nih.gov/{indices}',data)

                except IndexError:
                    connection.send_back("Fehler, bitte mit anderem Suchbegriff versuchen")

        else:
            connection.send_back("Dafür hab ich keinen Eintrag gefunden")





            '''#determin beginning and end of searched word and description
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
            connection.send_back(f'Ich konnte leider keine definition für {message[1]} finden', data)'''