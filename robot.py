import csv, time, clipboard
import json
from random import randrange
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# import emoji

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
validLetters = []
startWordChoices = ["penis", "audio", "irate", "soare", "roate", "raise", "slate", "sauce", "slice", "shale", "share",
                    "sooty", "shine", "suite", "crane", "reais", "blahs", "centu", "doggo", "arose", "earls", "laser"]
words = {}
wordsleft = -1
wordProbs = {'a': .078, 'b': .02, 'c': .04, 'd': .038, 'e': .11, 'f': .014, 'g': .03, 'h': .023, 'i': .082, 'j': .0021,
             'k': .025, 'l': .053, 'm': .027, 'n': .072, 'o': .061, 'p': .028, 'q': .0024, 'r': .073, 's': .087,
             't': .067, 'u': .033, 'v': .01, 'w': .0091, 'x': .0027, 'y': .016, 'z': .0044}


def init(filename):
    with open(filename, encoding='utf-8-sig') as f:
        csvreader = csv.reader(f)
        validWords = []
        for i in csvreader:
            validWords = i
        for i in validWords:
            words[i.lower()] = calculateProb(i.lower())
        wordsleft = len(validWords)
        print("We have " + str(wordsleft) + " words left to guess!")
    return startWordChoices[randrange(len(startWordChoices))]


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


def removeLetterNotInWord(letter, pos):
    remove = []
    for word in words.keys():
        if letter not in word:
            remove.append(word)
        elif word[pos] == letter:
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
    ret = 0
    for i in word:
        val = wordProbs[i]
        if word.count(i) > 1:
            val *= .1
        ret += val
    return ret


def chooseWord():
    highest = 0
    word = ''
    for i in words.keys():
        if words[i] > highest:
            highest = words[i]
            word = i
    return word


def playGame(startWord):
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    wordChosen = startWord
    tweet = ""
    webpage = driver.find_element(By.TAG_NAME, "body")

    webpage.click()
    time.sleep(1)
    webpage.send_keys(wordChosen)
    webpage.send_keys(Keys.RETURN)
    for i in range(0, 6):
        removeChar = []
        removePos = []
        removeNotIn = []
        removeMultiple = []

        correct = 0
        for j in range(5):
            tile = driver.find_element(By.XPATH, '//*[@id="wordle-app-game"]/div[1]/div/div[{}]/div[{}]/div'.format(i + 1, j+1))
            time.sleep(1)
            evaluation = tile.get_attribute("data-state")
            print(j, tile.get_attribute("data-state"), evaluation)
            if evaluation == "absent":
                tweet += 'b'
                if wordChosen[j] not in validLetters:
                    removeChar.append(wordChosen[j])
                else:
                    removeMultiple.append(wordChosen[j])
            elif evaluation == "present":
                tweet += 'y'
                validLetters.append(wordChosen[j])
                removeNotIn.append([wordChosen[j], j])
            else:
                correct += 1
                tweet += 'g'
                validLetters.append(wordChosen[j])
                removePos.append([wordChosen[j], j])
        tweet += '\n'
        words.pop(wordChosen, None)
        if correct == 5:
            driver.quit()
            return [i,tweet]

        for c in removeChar:
            if c not in validLetters:
                removeLetter(c)

        for p in removePos:
            removeSpecificPosition(p[0], p[1])

        for n in removeNotIn:
            removeLetterNotInWord(n[0], n[1])

        for m in removeMultiple:
            removeMultipleLetter(m)

        time.sleep(2)
        wordsleft = len(words.keys())
        print("We have " + str(wordsleft) + " words left to guess!")

        wordChosen = chooseWord()
        webpage.send_keys(wordChosen)
        print("word chosen:", wordChosen)

        webpage.send_keys(Keys.RETURN)
        print("return")
        driver.refresh()
        webpage = driver.find_element(By.TAG_NAME, "body")
        time.sleep(1)


def run(filename):
    word = init(filename)
    word = "penis"
    n = playGame(word)
    # collectInfo(filename)
    return n[0]
