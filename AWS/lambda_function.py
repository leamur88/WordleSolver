from wordleSolver import init, playGame
from twitterAPI import sendTweet

def lambda_handler(event, context):
    filename = 'supposedWords.csv'
    word = init(filename)
    response = playGame(word)
    print("Congratulations!!!! you made it out in " + str(response[0] + 1) + " moves.")
    reply_id = sendTweet(response[1], filename)
    print("tweet\n", response[1])
    return True

