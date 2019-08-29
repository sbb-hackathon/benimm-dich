#!/usr/bin/env python3

import tweepy
import logging
import random
from config import create_api
import time
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

KEYWORDS = ["Karriere", "Haushalt", "Liebe", "Intimität", "Alltagsprobleme", "FemaleTroubles", "Beauty"]

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue

        follow_user_if_cool_enough(tweet)    

        api.update_status(
            status=answer(tweet),
            in_reply_to_status_id=tweet.id_str,
        )
    return new_since_id

def follow_user_if_cool_enough(tweet):
    if (not tweet.user.following) and tweet.user.followers_count > 15:
        logger.info(f"Start to follow {tweet.user.name}")
        tweet.user.follow()

def answer(tweet, keywords):
    logger.info(f"Answering to {tweet.user.name}")

    if (keyword in tweet.text.lower() for keyword in KEYWORDS):
            
            #get all jsons with certain hashtag
            with open('data.json') as json_file:
                data = json.load(json_file)
                idxs = []
                for d in enumerate(data):
                    if keyword in d['hash']:
                            idxs+=[d['id']]
                            
            #random
            reply_id = random.choice(idxs)
    # if (keyword in tweet.text.lower() for keyword in keywords):
    #tweet.entities.hashtags
    return f"Hallo @{tweet.user.screen_name} " + time.strftime("%I:%M:%S")

def main():
    api = create_api()
    since_id = os.environ['TW_SINCE_ID']
    while True:
        print(since_id)
        since_id = check_mentions(api, since_id)
        os.environ['TW_SINCE_ID'] = since_id
        logger.info("Waiting...")
        time.sleep(10)

if __name__ == "__main__":
    main()