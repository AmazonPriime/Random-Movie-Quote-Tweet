import config as config
import tweepy, random, os, re, requests

current_dir = os.path.dirname(os.path.abspath(__file__))

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_key_secret)
auth.set_access_token(config.access_key, config.access_key_secret)
api = tweepy.API(auth)

status = "#Movie #Quote {}. {}: {}".format(title, character, quote)

api.update_with_media(status)
