import json
import csv
import time
import emoji
from random import randrange
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import shutil
import uuid
import boto3
from datetime import datetime
import datetime

validLetters = []
startWordChoices = ["penis", "audio", "irate", "soare", "roate", "raise", "slate", "sauce", "slice", "shale", "share",
                    "sooty", "shine", "suite", "crane", "reais", "blahs", "centu", "doggo", "arose", "earls", "laser"]
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


def lambda_handler(event, context):
    # instance_ = WebDriver()
    # driver = instance_.get()
    word = init('supposedWords.csv')
    print("Starting word:", word)
    n = playGame(word)
    print("Congratulations!!!! you made it out in " + str(n + 1) + " moves.")
    return True

def collectInfo(filename, n):
    driver.get("https://www.powerlanguage.co.uk/wordle/")
    # webpage = driver.find_element(By.CLASS_NAME, "nightmode")
    javascript1 = """return document
            .querySelector('game-app').shadowRoot
            .querySelector('game-theme-manager')
            .querySelector('#game')
            .querySelector('game-modal')
            .querySelector('game-stats').shadowRoot
            .querySelector('div.container')
            .querySelector('div.footer')
            .querySelector('div.share')
            """
    # javascript2 = """return document
    #             .querySelector('game-app').shadowRoot
    #             .querySelector('game-theme-manager')
    #             .querySelector('#game')
    #             .querySelector('game-modal')
    #             .querySelector('game-stats')
    #             """
    time.sleep(2)
    share = driver.execute_script(javascript1)
    # score = driver.execute_script(javascript2)
    share.find_element(By.ID, 'share-button').click()
    print("Share", share)
    print(clipboard.paste())

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


def playGame(startWord):
    driver.get("https://www.powerlanguage.co.uk/wordle/")
    wordChosen = startWord

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
                if wordChosen[j] not in validLetters:
                    removeChar.append(wordChosen[j])
                else:
                    removeMultiple.append(wordChosen[j])
            elif evaluation == "present":
                validLetters.append(wordChosen[j])
                removeNotIn.append([wordChosen[j], j])
            else:
                correct += 1
                validLetters.append(wordChosen[j])
                removePos.append([wordChosen[j], j])
        words.pop(wordChosen, None)
        if correct == 5:
            return i

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