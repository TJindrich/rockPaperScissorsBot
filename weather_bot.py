import tweepy  # Makes it easier to get data from twitter
import time  # Needed to put the bot to sleep
# NOTE: I put my keys in the keys.py to separate them
# from this main file.

from keys import *  # importing keys from an external .py file
import pyowm  # Weather

# NOTE: flush=True is just for running this script
# with PythonAnywhere's always-on task.
# More info: https://help.pythonanywhere.com/pages/AlwaysOnTasks/
print('this is my twitter bot', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
api_key = '3b57e8df0bf20d0a3183f5a06386eb86'
url = 'https://openweathermap.org/city/3068160'
FILE_NAME = 'last_seen_id.txt'

owm = pyowm.OWM(api_key)
plzen = owm.weather_at_place('Pilsen, CZ')
weather = plzen.get_weather()


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)

    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
        last_seen_id,
        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#pocasi' in mention.full_text.lower():
            print('found #pocasi!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                              ' V Plzni je právě: '+str(weather.get_temperature('celsius')['temp'])+' °C', mention.id)


while True:
    reply_to_tweets()
    time.sleep(15)
