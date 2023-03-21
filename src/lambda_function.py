import os
import json
import requests
import tweepy
import urllib.parse
from textwrap import dedent


def get_tweet():
    # Get a new word if there are two different readings (a slash in the word) since the japandict link won't work
    # OR get a new word if the meaning is empty
    # OR get a new word if the word is in katakana or has no kanji
    while True:
        response = requests.get("https://jlpt-vocab-api.vercel.app/api/words/random")
        data = response.json()
        if "/" not in data["word"] and data["meaning"] != "" and data["furigana"] != "" and "/" not in data["furigana"]:
            break

    word = data["word"]
    meaning = data["meaning"]
    furigana = data["furigana"]
    romaji = data["romaji"]
    level = data["level"]

    # Encode the URL
    encoded_word = urllib.parse.quote_plus(word)
    jisho_url = f"https://jisho.org/search/{encoded_word}"
    japandict_url = f"https://www.japandict.com/{encoded_word}"

    # Create the content of the tweet
    line_one = f"N{level}"
    line_two = f"{word}" if len(furigana) == 0 else f"{word} 【{furigana}】"
    line_three = f"{meaning}"
    line_four = f"#jlpt #japanese #日本語"
    line_five = f"{japandict_url}"

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