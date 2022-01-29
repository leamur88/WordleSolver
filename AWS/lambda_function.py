from wordleSolver import init, playGame
from twitterAPI import sendTweet

def lambda_handler(event, context):
    word = init('supposedWords.csv')
    response = playGame(word)
    print("Congratulations!!!! you made it out in " + str(response[0] + 1) + " moves.")
    reply_id = sendTweet(response[1], 0)
    print("tweet\n", response[1])
    return True

