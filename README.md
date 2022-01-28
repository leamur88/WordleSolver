# WordleSolver
Robot that can solve the Daily Wordle Automatically!

## Background
As I'm sure many of you know, wordle is a game where you try to guess a random 5-letter word with up to six guesses.
It is actually very simple to cheat and find the word right away if you do a little digging around in inspect element, 
but that's no fun. Instead, this robot can serve as a benchmark to see how good your word deducing skills are. There are 
two versions of this robot. The "smart" version has a word-bank of words that can only be used as the answer key within 
wordle. This word-bank is stored as "supposedWords.csv". The "dumb" version uses a much larger word-bank (stored in 
"validWords.csv") which contains all valid entries you can input into wordle. The dumb version has about 6x more words 
than the smart version and every word within the smart version exists in the dumb version. I got these lists by looking
at the network tab of inspect element on chrome and downloading the only js file that was sent from the server. A copy 
of this file is saved as "wordle.js" and you can scroll through it to find the lists for yourself if you'd like.

## Prerequisites
Must have selenium installed version == 4.1.0
chromium version == 97.0.4692

## How to run
Simply run the main.py file to start the robot. Comment out which word-bank you would like to use.

## How it works
Selenium starts up and then inputs the initial starting word into the wordle. From there, we do some simple html parsing
to see what letters are present, absent, or correct. If any letter is absent, we remove all words with that letter from
our dictionary. If a letter is present that implies that it is in the word we are looking for but not at that position. 
In this case we remove all words that don't contain this letter and all words that contain that letter in that position.
If a letter is correct we can remove all words that don't contain that letter in that position. This drastically reduces 
the word-bank even after 2 attempts. To decide which word to use next, each word has a value associated with it that is 
derived from the frequency of the letter within a dictionary. This means words with more e's and a's are likely to be
guessed next instead of words with j's and w's. Once the answer is guessed, the json is updated with the result and the 
wordle display is printed in the terminal.

## AWS
Currently using the tutorial from this [video](https://www.youtube.com/watch?v=jWqbYiHudt8) to set up my AWS Lambda 
environment.

## Future Expansion
* Tweet out daily wordle summary for each bot 
* ^Add this to Lambda Function
* Update word frequency calculation to reduce the value of words that have multiple of the same letter
