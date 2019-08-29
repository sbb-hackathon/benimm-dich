import tweepy
import logging
import os

logger = logging.getLogger()

def create_api():
    app_key = os.getenv("APP_KEY")
    app_secret = os.getenv("APP_SECRET")
    oauth_token = os.getenv("OAUTH_TOKEN")
    oauth_token_secret = os.getenv("OAUTH_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(app_key, app_secret)
    auth.set_access_token(oauth_token, oauth_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api