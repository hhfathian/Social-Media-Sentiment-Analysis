
from tweepy import OAuthHandler
from tweepy import Stream,API,Cursor
from tweepy.streaming import StreamListener
from datetime import datetime
import pandas as pd
from datetime import date
from datetime import timedelta
import pytz
from textblob import TextBlob

consumer_key = '****************'
consumer_secret = '****************'
access_token = '****************'
access_token_secret = '****************'

# Create authorization info
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = API(auth, wait_on_rate_limit=True)

search_words=['nature', 'sport', 'book', 'music']

today = str(date.today())
yesterday=str(date.today()- timedelta(days = 1))

tweets_df=[]

#Looping on the search words
for i in search_words:
    i+=" -filter:retweets"
    tweets = Cursor(api.search,tweet_mode='extended',q=i, since=yesterday, until=today).items(30000000000000000)
    users_locs = [[tweet.user.screen_name, tweet.user.time_zone, tweet.user.location, tweet.user.followers_count, tweet.user.friends_count,tweet.retweet_count,  tweet.user.created_at, tweet.created_at, tweet.full_text, tweet.favorite_count] for tweet in tweets]
    tweet_text = pd.DataFrame(data=users_locs, columns=['user', 'Time Zone', "location","followers", 'Following','Retweet count',"Register Date", "Tweet Date", 'Tweet', 'favorite_count'])
    tweets_df.append(tweet_text)

Finaltweets_df=pd.concat(tweets_df).reset_index()

Finaltweets_df['Create_atDate']=(datetime.datetime.now(pytz.timezone('Asia/Kolkata'))- timedelta(hours = 1)).strftime("%Y-%m-%d")

Finaltweets_df['Create_atTime']=(datetime.datetime.now(pytz.timezone('Asia/Kolkata'))- timedelta(hours = 1)).strftime("%H:%M:%S")

Finaltweets_df['RegisterDate']=[str(u) for u in pd.to_datetime(Finaltweets_df['Register Date']).dt.date]
Finaltweets_df['RegisterTime']=[str(u) for u in pd.to_datetime(Finaltweets_df['Register Date']).dt.time]
Finaltweets_df['TweetDate']=[str(u) for u in pd.to_datetime(Finaltweets_df['Tweet Date']).dt.date]
Finaltweets_df['TweetTime']=[str(u) for u in pd.to_datetime(Finaltweets_df['Tweet Date']).dt.time]

Finaltweets_df['Polarity_Number']=[TextBlob(u).sentiment.polarity for u in Finaltweets_df['Tweet']]
Finaltweets_df["SocialMediaType"]="Twitter"
Finaltweets_df['Polarity']=["Positive" if u>0 else  "Negative" if u<0 else "Neutral" for u in Finaltweets_df['Polarity_Number']]
Finaltweets_df['Tweet_Hour'] = pd.to_datetime(Finaltweets_df['Tweet Date']).dt.hour

Finaltweets_df['location']=Finaltweets_df['location'].fillna("Unknown")
Finaltweets_df['location']=[u.split(', ',1)[0] for u in Finaltweets_df.location]
