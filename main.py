import config as config
import tweepy, random, os, re, requests
import json, pprint, bitly_api

current_dir = os.path.dirname(os.path.abspath(__file__))

def getQuotes(file):
    with open("{}/{}".format(current_dir, file)) as f:
        quotes = json.load(f)
    return quotes

def getRandomMovie(quotes):
    movie_list = list(quotes.items())
    rand = random.randint(0, len(movie_list) - 1)
    movie = movie_list[rand]
    if len(movie[1]["quotes"]) == 0:
        getRandomMovie(quotes)
    return movie[0], movie[1]

def getRandomQuote(quotes):
    quotes = quotes["quotes"]
    rand = random.randint(0, len(quotes) - 1)
    return quotes[rand]["character"], quotes[rand]["quote"]

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_key_secret)
auth.set_access_token(config.access_key, config.access_key_secret)
api = tweepy.API(auth)
b = bitly_api.Connection(config.api_user, config.api_key)

status = ""
while len(status) <= 0 or len(status) >= 275:
    quotes = getQuotes("scraper/quotes.json")
    title, quotes = getRandomMovie(quotes)
    year, id = quotes["year"], quotes["id"]
    character, quote = getRandomQuote(quotes)
    url = "https://www.imdb.com/title/{}/".format(id)
    response = b.shorten(uri = url)
    status = "#Movie #Quote {} ({}). {}: {} {}".format(title, year, character, quote, response['url'])

api.update_status(status)
