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

KEYWORDS = ["karriere", "haushalt", "liebe", "sex", "familie", "alltagsprobleme", "femaletroubles", "beauty", "couplegoals"]

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue

        follow_user_if_cool_enough(tweet)    

        try:
            api.update_status(
            status=answer(tweet)[0:280],
            in_reply_to_status_id=tweet.id_str
            )
        except:
            return new_since_id

    return new_since_id

def follow_user_if_cool_enough(tweet):
    if (not tweet.user.following) and tweet.user.followers_count > 15:
        logger.info(f"Start to follow {tweet.user.name}")
        tweet.user.follow()

def answer(tweet):
    logger.info(f"Answering to {tweet.user.name}")

    print(list(map(lambda hashtag: hashtag["text"].lower(), tweet.entities["hashtags"])))
    for hashtag in map(lambda hashtag: hashtag["text"].lower(), tweet.entities["hashtags"]):
        if hashtag in KEYWORDS:
            return f"@{tweet.user.screen_name} {quote(hashtag)}"
    
    return f"@{tweet.user.screen_name} {random_quote()}"

def quote(hashtag):
    matching_quotes = list(filter(lambda o: hashtag in o['hash'], input_json()))
    if matching_quotes:
        selected_quote = random.choice(matching_quotes)
        return f"{selected_quote['cont']} – ({selected_quote['year']}) {selected_quote['link']}"
    else:
        return random_quote()

def random_quote():
    selected_quote = random.choice(input_json())
    return f"{selected_quote['cont']} – ({selected_quote['year']}) {selected_quote['link']}"

def input_json():
    with open('data.json') as json_file:
        return json.load(json_file)

def main():
    api = create_api()
    since_id = int(os.environ['TW_SINCE_ID'])
    while True:
        print(since_id)
        since_id = check_mentions(api, since_id)
        os.environ['TW_SINCE_ID'] = str(since_id)
        logger.info("Waiting...")
        time.sleep(20)

if __name__ == "__main__":
    main()