

import pandas as pd
import instaloader
from datetime import datetime
from datetime import timedelta
from textblob import TextBlob
from datetime import date
import pytz
import numpy as np

L = instaloader.Instaloader(download_pictures=False,
                            download_video_thumbnails=False,
                            download_videos=False,
                            download_geotags=True,
                            download_comments=False,
                            save_metadata=True
                            )
L.login('your instagram account', 'your password')
posts = instaloader.Hashtag.from_name(L.context, "The hashtag you are looking for").get_posts()

SINCE = date.today()- timedelta(days = 2)  
UNTIL = date.today()- timedelta(days = 1) 

User=[]
location=[]
PostDate=[]
Post=[]
favorite_count=[]

#INCE = datetime(2020, 7, 5)  # further from today, inclusive
#UNTIL = datetime(2020, 7, 6)  # closer to today, not inclusive

k = 0  # initiate k
k_list = []  # uncomment this to tune k

for post in posts:
    postdate = post.date.date()

    if postdate > UNTIL:
        continue
    elif postdate <= SINCE:
        k += 1
        if k == 20:
            break
        else:
            continue
    else:
        User.append(post.profile)
        location.append(post.location)
        PostDate.append(post.date)
        Post.append(post.caption)
        favorite_count.append(post.likes)
        k = 0  # set k to 0

InstagramPosts=pd.DataFrame()

InstagramPosts["user"]=User
InstagramPosts["Time Zone"]=''
InstagramPosts["location"]=[u[1] if u!=None else np.nan for u in location]
InstagramPosts["followers"]=''
InstagramPosts["Following"]=''
InstagramPosts["RegisterDate"]=''
InstagramPosts["RegisterTime"]=''
InstagramPosts["PostDate"]=PostDate
InstagramPosts['PostTime']=[str(u) for u in pd.to_datetime(InstagramPosts['PostDate']).dt.time]
InstagramPosts['PostDate']=[str(u) for u in pd.to_datetime(InstagramPosts['PostDate']).dt.date]
InstagramPosts["Post"]=Post
InstagramPosts["favorite_count"]=favorite_count
InstagramPosts['Create_atDate']=(datetime.now(pytz.timezone('Asia/Kolkata'))- timedelta(hours = 1)).strftime("%Y-%m-%d")
InstagramPosts['Create_atTime']=(datetime.now(pytz.timezone('Asia/Kolkata'))- timedelta(hours = 1)).strftime("%H:%M:%S")
InstagramPosts['Polarity_Number']=[TextBlob(u).sentiment.polarity if u!=None else 0 for u in InstagramPosts['Post']]
InstagramPosts["SocialMediaType"]='Instagram'
InstagramPosts['Polarity']=["Positive" if u>0 else  "Negative" if u<0 else "Neutral" for u in InstagramPosts['Polarity_Number']]
InstagramPosts['Post_Hour'] = pd.to_datetime(InstagramPosts['PostTime']).dt.hour
InstagramPosts['location']=InstagramPosts['location'].fillna("Unknown")
InstagramPosts['location']=[u.split(', ',1)[0] for u in InstagramPosts.location]
