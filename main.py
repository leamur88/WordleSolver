import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

words = {}
wordsleft = -1
lettersKnown = {}
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
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://www.powerlanguage.co.uk/wordle/")
        print(driver.title)


def calculateProb(word):
    ret = 0
    for i in word:
        ret += wordProbs[i]
    return ret


if __name__ == '__main__':
    init()
    highest = ''
    highestprob = 0
    for i in words.keys():
        if words[i] > highestprob:
            highestprob = words[i]
            highest = i
    print(highest)
    # for i in range(6):
    # guess = input("What would you like your guess to be? ")
