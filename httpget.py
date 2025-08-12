
import requests

urban = str(input())
arr  = urban.split(' ')


if arr[0] == ".urban":
    search = arr[1]

    contents = requests.get(f'https://unofficialurbandictionaryapi.com/api/search?term={search}&limit=1&page=1&')

    contentStr = str(contents.content)
    status = int(contents.status_code)
    #print(contentStr)
    #print(status)

    if status == 200:

        indexWord = contentStr.index('"word"')
        indexWordEnd = contentStr.index('","meaning"')
        indexMeaning = contentStr.index('"meaning"')
        indexMeaningEnd = contentStr.index('","example"')

        WordStr = contentStr[indexWord:indexWordEnd]
        MeaningStr = contentStr[indexMeaning:indexMeaningEnd]
        WordSplit = WordStr.split('":"')
        MeaningSplit = MeaningStr.split('":"')



        print(f'Word: {WordSplit[1]}')
        print(f'Meaning: {MeaningSplit[1]}')

    else:
        print("Error - No Definition Found")

