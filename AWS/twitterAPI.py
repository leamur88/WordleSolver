import json
import boto3
from requests_oauthlib import OAuth1Session
from datetime import date

s3 = boto3.client('s3')
bucket = 'wordlesolvertwitter'


def postTweet(consumer_token, consumer_key, access_token, access_token_secret, payload):
    oauth = OAuth1Session(
        consumer_token,
        client_secret=consumer_key,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))
    # Saving the response as JSON
    return response.json()


def createPayload(msg, reply):
    if reply != 0:
        return {
            "text": msg,
            "reply": {
                "in_reply_to_tweet_id": str(reply)
            }
        }
    else:
        return {"text": msg}


def createMessage(fname, wordleday, message):
    if fname == "supposedWords.csv":
        msg = "Smart Robot, Wordle Day " + str(wordleday)
        msg += "\n\n" + message
        msg += "\n#wordle #wordlebot"
        return msg
    else:
        msg = "Not as Smart Robot, Wordle Day " + str(wordleday)
        msg += "\n\n" + message
        msg += "\n#wordle #wordlebot"
        return msg


def sendTweet(message, fname, reply_id):
    secretsFile = s3.get_object(Bucket=bucket, Key='secretsWordle.json')
    secretsContent = secretsFile['Body']

    secrets = json.loads(secretsContent.read())

    replyID = reply_id
    wordleDay = 223 + (date.today() - date(2022,1,28)).days

    ct = secrets['consumer_token']
    ck = secrets['consumer_key']
    at = secrets['access_token']
    ats = secrets['access_key']

    msg = createMessage(fname, wordleDay, message)

    payload = createPayload(msg, replyID)
    partial_response = postTweet(ct, ck, at, ats, payload)
    new_reply_id = partial_response['data']['id']
    return new_reply_id
