#!/usr/bin/env python

import tweepy
import logging
from config import create_api
import time
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if (keyword in tweet.text.lower() for keyword in keywords):
            logger.info("Answering to {tweet.user.name}")
            
            #get all jsons with certain hashtag
            with open('data.json') as json_file:
                data = json.load(json_file)
                idxs = []
                i=0
                for i,d in enumerate(data):
                    if keyword in d['hashtags']:
                            idxs=i
                            
            #random

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                status="Please reach us via DM",
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        print(since_id)
        since_id = check_mentions(api, ["help", "support"], since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()