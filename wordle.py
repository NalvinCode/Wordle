from array import array
import random


import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


#Cantidad maxima de oportunidades#
MAX_GUESSES = 6

#Longitud de palabras#
WORD_LEN = 5

#Ids de colores#
BLACK_ID = 1
GREEN_ID = 2
YELLOW_ID = 3

#Elecciones menu#
PLAY_GAME = 1
GAME_RULES = 2

RETRY = 1
MAIN_MENU = 2
EXIT_GAME = 3

NEXT_LEVEL = 1

#Reglas del juego#
RULES = "REGLAS:\nLa idea del juego es ingresar palabras hasta adivinar la correcta, teniendo en consideracion las siguientes situaciones:\nSi la letra aparece en verde, es porque la has acertado y está en la palabra, y también está en la casilla correcta de la palabra.\nSi la letra aparece en amarillo, es porque está en la palabra, pero no está en la casilla correcta.\nSi la letra aparece en amarillo es porque no has acertado, y no está en la palabra que tienes que adivinar."


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


def getSave():
    #Obtengo listado de palabras ya adivinadas#
    try:
        saves = open("common\saves.txt", "rt", encoding="UTF8")
        saveList = []
        for line in saves:
            line = line.rstrip("\n")
            line = line.split()
            for word in line:
                saveList.append(word)
    except OSError as messege:
        print("Error al abrir archivo de palabras adivinadas", messege)
    finally:
        try:
            saves.close()
        except NameError:
            pass

    return saveList


def saveWord(word):
    #Guardo palabra adivinada#
    try:
        saves = open("common\saves.txt", "at", encoding="UTF8")
        saves.write(word + ' ')
    except OSError as messege:
        print("Error al grabar archivo de palabras adivinadas", messege)
    finally:
        try:
            saves.close()
        except NameError:
            pass


def initMenu():
    print(Fore.RED + "Wordle")
    print()
    print("Elija una opcion")
    selection = int(
        input("-Jugar (1)\n-Como jugar (2)\n-Salir (3)\n"))

    if selection == PLAY_GAME:
        initGame()

    if selection == GAME_RULES:
        print(RULES)

    if selection == EXIT_GAME:
        return


def initGame():
    #Obtengo lista de palabras del juego#
    wordList = getWordList()
    #Obtengo lista de palabras ya adivinadas#
    saveList = getSave()

    #Filtro palabras ya adivinadas de la lista de palabras#
    wordList = list(filter(lambda w: w not in saveList, wordList))

    #Obtengo palabra aleatoria de la lista filtrada#
    word = wordList[random.randint(0, len(wordList) - 1)]

    #Inicializo el tablero#
    board = [["_", "_", "_", "_", "_"],
             ["_", "_", "_", "_", "_"],
             ["_", "_", "_", "_", "_"],
             ["_", "_", "_", "_", "_"],
             ["_", "_", "_", "_", "_"],
             ["_", "_", "_", "_", "_"]]

    #Inicializo matriz de colores#
    coloredWords = [["_", "_", "_", "_", "_"],
                    ["_", "_", "_", "_", "_"],
                    ["_", "_", "_", "_", "_"],
                    ["_", "_", "_", "_", "_"],
                    ["_", "_", "_", "_", "_"],
                    ["_", "_", "_", "_", "_"]]

    #Inicio el nivel#
    startLevel(board, word, coloredWords)


def startLevel(board, word, coloredWords):
    #Testeo#
    print(word)

    printBoard(coloredWords, board)
    guesses = 0
    while(guesses < MAX_GUESSES):
        guess = str(input("Ingrese palabra: ")).upper()

        if not validWord(guess):
            continue

        for i in range(len(guess)):
            board[guesses][i] = guess[i]
            coloredWords[guesses].append(BLACK_ID)
            if(guess[i] in word):
                coloredWords[guesses][i] = YELLOW_ID
            if (guess[i] == word[i]):
                coloredWords[guesses][i] = GREEN_ID
        guesses += 1
        printBoard(coloredWords, board)

        #Si la palabra es correcta, termino el nivel#
        if word == guess:
            break

    #Si el jugador perdio el nivel, doy opciones#
    if word != guess:
        print("GAME OVER")
        print()
        choose = int(
            input("Reintentar nivel?\n-Reintentar (1)\n-Menu principal (2)\n"))

        while choose not in [RETRY, MAIN_MENU]:
            choose = int(
                input("Opcion incorrecta\n-Reintentar (1)\n-Menu principal (2)\n"))

        if(choose == RETRY):
            initGame()
            return

        initMenu()
        return

    #Guardo progreso#
    saveWord(word)

    choose = int(
        input("PALABRA CORRECTA\n-Siguiente nivel (1)\n-Menu principal (2)\n"))

    while choose not in [NEXT_LEVEL, MAIN_MENU]:
        choose = int(
            input("Opcion incorrecta\n-Siguiente nivel (1)\n-Menu principal (2)\n"))

    if choose == NEXT_LEVEL:
        initGame()
        return

    initMenu()
    return


def printBoard(coloredWords, board):
    for i in range(len(board)):
        for z in range(len(board[i])):
            if(coloredWords[i][z] == BLACK_ID):
                print(Fore.BLACK + board[i][z], end=' ')
                continue
            if(coloredWords[i][z] == YELLOW_ID):
                print(Fore.YELLOW + board[i][z], end=' ')
                continue
            if(coloredWords[i][z] == GREEN_ID):
                print(Fore.GREEN + board[i][z], end=' ')
                continue
            print(board[i][z], end=' ')
        print()


def validWord(word):
    wordList = getWordList()

    if (len(word) > WORD_LEN) or (len(word) < WORD_LEN):
        print("Palabra invalida")
        return False

    if(word not in wordList):
        print("Palabra inexistente")
        return False

    return True


#Programa principal#
initMenu()
