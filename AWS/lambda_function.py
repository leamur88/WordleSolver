from wordleSolver import init, playGame
from twitterAPI import sendTweet
import json, boto3, os, sys, uuid

def lambda_handler(event, context):
    if event["robot"] == "smart":
        filename = 'supposedWords.csv'
        reply_id = 0
        print(reply_id)
    else:
        s4 = boto3.client('s3')
        filename = 'validWords.csv'
        replyFile = s4.get_object(Bucket='wordlesolvertwitter', Key='reply_id.txt')
        reply_id = int(replyFile['Body'].read())
    word = init(filename)
    response = playGame(word)
    print("Congratulations!!!! you made it out in " + str(response[0] + 1) + " moves.")
    new_reply_id = sendTweet(response[1], filename, reply_id)
    string = str(new_reply_id)
    encoded_string = string.encode("utf-8")
    s3 = boto3.resource("s3")
    bucket_name = "wordlesolvertwitter"
    file_name = "reply_id.txt"
    s3_path = file_name
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    print("tweet\n", response[1])
    return True

