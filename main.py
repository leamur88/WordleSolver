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
validLetters = []
# startWord = "irate"
# startWord = "audio"
startWord = "penis"
words = {}
wordsleft = -1
wordProbs = {'a': .078, 'b': .02, 'c': .04, 'd': .038, 'e': .11, 'f': .014, 'g': .03, 'h': .023, 'i': .082, 'j': .0021,
             'k': .025, 'l': .053, 'm': .027, 'n': .072, 'o': .061, 'p': .028, 'q': .0024, 'r': .073, 's': .087,
             't': .067, 'u': .033, 'v': .01, 'w': .0091, 'x': .0027, 'y': .016, 'z': .0044}


def init():
    # with open('supposedWords.csv', encoding='utf-8-sig') as f:
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
        removeChar = []
        removePos = []
        removeNotIn = []
        removeMultiple = []

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
        correct = 0
        for j in range(5):
            evaluation = board[j].get_attribute("evaluation")
            print(j, board[j].get_attribute("letter"), evaluation)
            if evaluation == "absent":
                if wordChosen[j] not in validLetters:
                    removeChar.append(wordChosen[j])
                else:
                    removeMultiple.append(wordChosen[j])
            elif evaluation == "present":
                validLetters.append(wordChosen[j])
                removeNotIn.append(wordChosen[j])
            else:
                correct += 1
                validLetters.append(wordChosen[j])
                removePos.append([wordChosen[j], j])
        words.pop(wordChosen)

        if correct == 5:
            return i

        for c in removeChar:
            if c not in validLetters:
                removeLetter(c)

        for p in removePos:
            removeSpecificPosition(p[0], p[1])

        for n in removeNotIn:
            removeLetterNotInWord(n)

        for m in removeMultiple:
            removeMultipleLetter(m)

        time.sleep(5)
        wordsleft = len(words.keys())
        print("We have " + str(wordsleft) + " words left to guess!")

        wordChosen = chooseWord()
        webpage.send_keys(wordChosen)
        print("word chosen:", wordChosen)
        time.sleep(5)

        webpage.send_keys(Keys.RETURN)
        print("return")
        driver.refresh()
        webpage = driver.find_element(By.CLASS_NAME, "nightmode")
        time.sleep(6)


def removeMultipleLetter(letter):
    remove = []
    for word in words.keys():
        if word.count(letter) >= 2:
            remove.append(word)
    for i in remove:
        words.pop(i)

def removeSpecificPosition(letter, pos):
    remove = []
    for word in words.keys():
        if word[pos] != letter:
            remove.append(word)
    for i in remove:
        words.pop(i)


def removeLetterNotInWord(letter):
    remove = []
    for word in words.keys():
        if letter not in word:
            remove.append(word)
    for i in remove:
        words.pop(i)

def removeLetter(letter):
    remove = []
    for word in words.keys():
        if letter in word:
            remove.append(word)
    for i in remove:
        words.pop(i)


def calculateProb(word):
    ret = 1
    for i in word:
        ret *= wordProbs[i]
    return ret


def chooseWord():
    highest = 0
    word = ''
    for i in words.keys():
        if words[i] > highest:
            highest = words[i]
            word = i
    return word

if __name__ == '__main__':
    init()
    print(len(words.keys()))
    # print(chooseWord())
    num = playGame()
    print("Congratulations!!!! you made it out in " + str(num + 1) + " moves.")
    # for i in range(6):
    # guess = input("What would you like your guess to be? ")
