def getWordList():
    #Obtengo listado de palabras#
    try:
        words = open("common\words.txt", "rt", encoding="UTF8")
        wordList = []
        for line in words:
            line = line.rstrip("\n")
            line = line.split()
            for word in line:
                wordList.append(word)
    except OSError as messege:
        print("Error al abrir archivo de palabras", messege)
    finally:
        try:
            words.close()
        except NameError:
            pass

    return wordList


def findWord(wordList):
    for i in range(len(wordList)):
        for z in range(len(wordList[i])):
            if(wordList[i].count(wordList[i][z]) >= 2 and wordList[i][z] == "A"):
                print(wordList[i])
                break


findWord(getWordList())
