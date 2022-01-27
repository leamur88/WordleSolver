from robot import run

if __name__ == '__main__':
    num = run('supposedWords.csv')
    # num = run('validWords.csv')
    print("Congratulations!!!! you made it out in " + str(num + 1) + " moves.")
