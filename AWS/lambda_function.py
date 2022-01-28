from wordleSolver import init, playGame
def lambda_handler(event, context):
    word = init('supposedWords.csv')
    print("Starting word:", word)
    response = playGame(word)
    print("Congratulations!!!! you made it out in " + str(response[0] + 1) + " moves.")
    print("tweet\n", response[1])
    return True

