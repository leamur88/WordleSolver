import csv, time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

startWord = "penis"
words = {}
wordsleft = -1
wordProbs = {'a': .078, 'b': .02, 'c': .04, 'd': .038, 'e': .11, 'f': .014, 'g': .03, 'h': .023, 'i': .082, 'j': .0021,
             'k': .025, 'l': .053, 'm': .027, 'n': .072, 'o': .061, 'p': .028, 'q': .0024, 'r': .073, 's': .087,
             't': .067, 'u': .033, 'v': .01, 'w': .0091, 'x': .0027, 'y': .016, 'z': .0044}


def init():
    with open('validWords.csv') as f:
        csvreader = csv.reader(f)
        validWords = []
        for i in csvreader:
            validWords = i
        for i in validWords:
            words[i.lower()] = calculateProb(i.lower())
        wordsleft = len(validWords)
        print("We have " + str(wordsleft) + " words left to guess!")


def playGame():
    driver.get("https://www.powerlanguage.co.uk/wordle/")
    wordChosen = startWord
    webpage = driver.find_element(By.CLASS_NAME, "nightmode")

    webpage.click()
    time.sleep(1)
    webpage.send_keys(wordChosen)
    webpage.send_keys(Keys.RETURN)
    for i in range(0, 6):

        javascript = """return document
        .querySelector('game-app').shadowRoot
        .querySelector('game-theme-manager')
        .querySelector('#game')
        .querySelector('#board-container')
        .querySelector('#board')
        .querySelectorAll('game-row')[{}].shadowRoot
        .querySelector('div.row')
        .querySelectorAll('game-tile')
        """.format(i)

        board = driver.execute_script(javascript)
        print(len(board))
        for j in range(5):
            evaluation = board[j].get_attribute("evaluation")
            if evaluation == "absent":
                removeLetter(wordChosen[j], False)
            elif evaluation == "present":
                removeLetter(wordChosen[j], True)
            else:
                removeLetter(wordChosen[j], True, j)

        time.sleep(2)
        wordsleft = len(words.keys())
        print("We have " + str(wordsleft) + " words left to guess!")

        wordChosen = chooseWord()
        webpage.send_keys(wordChosen)
        webpage.send_keys(Keys.RETURN)
        time.sleep(1)


def removeLetter(letter, inWord, pos=-1):
    if inWord:
        if pos > -1:
            for word in words.keys():
                if word[pos] != letter:
                    words.pop(word)
        else:
            for word in words.keys():
                if letter not in word:
                    words.pop(word)
    else:
        for word in words.keys():
            if letter in word:
                words.pop(word)


def calculateProb(word):
    ret = 0
    for i in word:
        ret *= wordProbs[i]
    return ret


def chooseWord():
    highest = 0
    word = ''
    for i in words.keys():
        if words[i] > highest:
            highest = word[i]
            word = i
    return word

if __name__ == '__main__':
    init()
    print(len(words.keys()))
    playGame()
    # for i in range(6):
    # guess = input("What would you like your guess to be? ")
