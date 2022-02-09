import json
import csv
import time
import emoji
from random import randrange
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import boto3


validLetters = []
smartStartWordChoices = ["penis", "audio", "irate", "soare", "roate", "raise", "slate", "sauce", "slice", "shale", "share",
                    "sooty", "shine", "suite", "crane", "reais", "blahs", "centu", "doggo", "arose", "earls", "laser"]
dumbStartWordChoices = ["penis", "farts", "pussy", "stinky"]
words = {}
wordsleft = -1
wordProbs = {'a': .078, 'b': .02, 'c': .04, 'd': .038, 'e': .11, 'f': .014, 'g': .03, 'h': .023, 'i': .082, 'j': .0021,
             'k': .025, 'l': .053, 'm': .027, 'n': .072, 'o': .061, 'p': .028, 'q': .0024, 'r': .073, 's': .087,
             't': .067, 'u': .033, 'v': .01, 'w': .0091, 'x': .0027, 'y': .016, 'z': .0044}


chromeOptions = Options()

chromeOptions.binary_location = '/opt/headless-chromium'
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--no-sandbox')
chromeOptions.add_argument('--start-maximized')
chromeOptions.add_argument('--start-fullscreen')
chromeOptions.add_argument('--single-process')
chromeOptions.add_argument('--disable-dev-shm-usage')
driver = Chrome('/opt/chromedriver', options=chromeOptions)


def init(filename):
    bucket = "wordlesolvertwitter"
    key = filename
    s3_resource = boto3.resource('s3')
    s3_object = s3_resource.Object(bucket, key)
    data = s3_object.get()['Body'].read().decode('utf-8-sig').splitlines()
    csvreader = csv.reader(data)
    validWords = []
    for i in csvreader:
        validWords = i
    for i in validWords:
        words[i.lower()] = calculateProb(i.lower())
    wordsleft = len(validWords)
    print("We have " + str(wordsleft) + " words left to guess!")
    if filename == "supposedWords.csv":
        return smartStartWordChoices[randrange(len(smartStartWordChoices))]
    else:
        print("hello??")
        return dumbStartWordChoices[randrange(len(dumbStartWordChoices))]


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
    driver.get("https://www.powerlanguage.co.uk/wordle/")
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

        javascript = """return document
        .querySelector('game-app').shadowRoot
        .querySelector('game-theme-manager')
        .querySelector('#game')
        .querySelector('#board-container')
        .querySelector('#board')
        .querySelectorAll('game-row')[{}].shadowRoot
        .querySelector('div.row')
        .querySelectorAll('game-tile')
        """

        board = driver.execute_script(javascript.format(i))
        correct = 0
        for j in range(5):
            evaluation = board[j].get_attribute("evaluation")
            print(j, board[j].get_attribute("letter"), evaluation)
            if evaluation == "absent":
                tweet += emoji.emojize(":black_large_square:")
                if wordChosen[j] not in validLetters:
                    removeChar.append(wordChosen[j])
                else:
                    removeMultiple.append(wordChosen[j])
            elif evaluation == "present":
                tweet += emoji.emojize(":yellow_square:")
                validLetters.append(wordChosen[j])
                removeNotIn.append([wordChosen[j], j])
            else:
                correct += 1
                tweet += emoji.emojize(":green_square:")
                validLetters.append(wordChosen[j])
                removePos.append([wordChosen[j], j])
        tweet += '\n'
        words.pop(wordChosen, None)
        if correct == 5:
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