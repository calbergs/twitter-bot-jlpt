import os
import json
import pyshorteners
import requests
import tweepy
from textwrap import dedent


def get_tweet():
    response = requests.get("https://jlpt-vocab-api.vercel.app/api/words/random")
    data = response.json()

    word = data["word"]
    meaning = data["meaning"]
    furigana = data["furigana"]
    romaji = data["romaji"]
    level = data["level"]

    # Shorten the Jisho URL
    long_url = f"https://jisho.org/search/{word}"
    type_tiny = pyshorteners.Shortener()
    short_url = type_tiny.tinyurl.short(long_url)

    # Create the content of the tweet
    line_one = f"N{level}"
    line_two = f"{word}" if len(furigana) == 0 else f"{word} 【{furigana}】"
    line_three = f"{meaning}"
    line_four = f"jisho: {short_url}"
    line_five = f"#jlpt #japanese #日本語"

    text = """
    {line_one}\n
    {line_two}\n
    {line_three}\n
    {line_four}\n
    {line_five}
    """.format(
        line_one=line_one,
        line_two=line_two,
        line_three=line_three,
        line_four=line_four,
        line_five=line_five,
    )
    tweet = dedent(text).strip("\n")
    return tweet

def lambda_handler(event, context):
    print("Get credentials")
    api_key = os.getenv("API_KEY")
    api_key_secret = os.getenv("API_SECRET_KEY")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    print("Authenticate")
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print("Get tweet")
    tweet = get_tweet()

    print(f"Post tweet: {tweet}")
    api.update_status(tweet)

    return {"statusCode": 200, "tweet": tweet}