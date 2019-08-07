import tweepy
import json
import telegram
from datetime import datetime, timezone
import re

with open('credentials.json') as f:
    creds = json.load(f)

#def utc_to_local(utc_dt):
#    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def deEmojify(inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')

def volume_catcher(message):
    try:
        x = re.search("[Sell|Buy] (.*) @", message).group(1)
        if "+" in x:
            value = 0
            for number in x.split("+"):
                value += int(number.replace(",",""))
            return value
        else:
            return int(x.replace(",",""))
    except AttributeError:
        return 0

auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
auth.set_access_token(creds['ACCESS_KEY'], creds['ACCESS_SECRET'])
api = tweepy.API(auth)

bot = telegram.Bot(token=creds['TELEGRAM_KEY'])

accounts_id = ["1038355836416929792", "4041496403", "1146918528328568833"]
chat_id='-1001225293643'

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if 'extended_tweet' in status._json:
            tweet = status.extended_tweet["full_text"]
        else:
            tweet = status.text

        message = f'{tweet}'
        message = deEmojify(message)
        message = message.split("~")[0]
        message = re.sub("http\S+", "", message)

        if "Okcoin" in message or "RT @" in message:
            pass
        elif volume_catcher(message) >= 40000 or volume_catcher(message) == 0:
            if not "XBT" in message or "XBTUSD" in message:
                if message.startswith("Liquidated"):
                    bot.send_message(chat_id=chat_id, parse_mode='HTML', text=message)
                else:
                    pass
            else:
                pass
        else:
            pass

    def on_error(self, status_code):
        if status_code == 420:
           bot.send_message(chat_id=chat_id, text='Stop and reestabilish the connection') 


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

#uncoment to track the accounts you want to

myStream.filter(follow=accounts_id)
