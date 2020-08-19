import tweepy
import time
import random
from keys import *

print('this is my twitter bot', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id2.txt'


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
    # DEV NOTE: use 1060651988453654528 for testing.
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
        if '#kamen' in mention.full_text.lower():
            rand = random.randrange(1, 3)
            print('found #kamen!', flush=True)
            print('responding back...', flush=True)
            if rand == 1:
                api.update_status('@' + mention.user.screen_name +
                                  ' Kámen! Remíza! Ještě jednou!', mention.id)
            if rand == 2:
                api.update_status('@' + mention.user.screen_name +
                                  ' Nůžky! Vyhrál jsi! Ještě jednou!', mention.id)
            if rand == 3:
                api.update_status('@' + mention.user.screen_name +
                                  ' Papír! Ha, vyhrál jsem! Ještě jednou!', mention.id)
        if '#nuzky' in mention.full_text.lower():
            rand = random.randrange(1, 3)
            print('found #nuzky!', flush=True)
            print('responding back...', flush=True)
            if rand == 1:
                api.update_status('@' + mention.user.screen_name +
                                  ' Nůžky! Remíza! Ještě jednou!', mention.id)
            if rand == 2:
                api.update_status('@' + mention.user.screen_name +
                                  ' Papír! Vyhrál jsi! Ještě jednou!', mention.id)
            if rand == 3:
                api.update_status('@' + mention.user.screen_name +
                                  ' Kámen! Ha, vyhrál jsem! Ještě jednou!', mention.id)
        if '#papir' in mention.full_text.lower():
            rand = random.randrange(1, 3)
            print('found #papir!', flush=True)
            print('responding back...', flush=True)
            if rand == 1:
                api.update_status('@' + mention.user.screen_name +
                                  ' Papír! Remíza! Ještě jednou!', mention.id)
            if rand == 2:
                api.update_status('@' + mention.user.screen_name +
                                  ' Kámen! Vyhrál jsi! Ještě jednou!', mention.id)
            if rand == 3:
                api.update_status('@' + mention.user.screen_name +
                                  ' Nůžky! Ha, vyhrál jsem! Ještě jednou!', mention.id)


while True:
    reply_to_tweets()
    time.sleep(15)
