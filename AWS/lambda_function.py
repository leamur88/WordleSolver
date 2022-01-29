from wordleSolver import init, playGame
import json
from twitterAPI import sendTweet

def lambda_handler(event, context):
    filename = 'supposedWords.csv'
    word = init(filename)
    response = playGame(word)
    print("Congratulations!!!! you made it out in " + str(response[0] + 1) + " moves.")
    reply_id = sendTweet(response[1], filename)
    updateResults(filename, reply_id, str(response[0]))
    print("tweet\n", response[1])
    return True

def updateResults(filename, reply_id, n):
    with open('results.json', 'r+') as f:
        data = json.load(f)
        if filename == 'validWords.csv':
            data["dumb"][n] += 1
            data["wordleDay"] += 1
        else:
            data["smart"][n] += 1
            data["replyID"] = reply_id

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
        f.close()
