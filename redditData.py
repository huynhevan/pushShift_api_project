from psaw import PushshiftAPI
import pandas
import csv
import json
import requests
import string
import re
from requests.api import post
api = PushshiftAPI();

import datetime as dt;


#url = 'https://api.pushshift.io/reddit/search/submission/?after=1626162766&before=1626249166&subreddit=seahawks'


def getPushShiftData(after, before, subreddit):
    url = 'https://api.pushshift.io/reddit/search/submission/?after='+str(after)+'&before='+str(before)+'&subreddit='+str(subreddit)
    #print(url)
    r = requests.get(url)
    print(r.text)
    print("hi")
    data = json.loads(r.text);
    return data['data']

def cleanText(text):
    # remove punctuation except $
    cleaned = text.translate(str.maketrans(' ', ' ', string.punctuation.replace('$','') + '’')).lower()
    # remove links (http)
    cleaned = re.sub("http\w+", " ", cleaned)
    # remove digits
    cleaned = cleaned.translate({ord(k): None for k in string.digits})
    # remove tabs/newlines
    cleaned = cleaned.replace("\n", " ").replace("\t", " ").strip()
    # remove double space
    cleaned = re.sub(' +', ' ', cleaned)
    return cleaned

def parseData(post):
    postData = list()
    try:
        title = cleanText(post['title'])
    except KeyError:
        title = "NaN"
    sub_id = post['id']
    #author = post['author']
    created = dt.datetime.fromtimestamp(post['created_utc'])
    postData.append((sub_id, title, created))
    postStats[sub_id] = postData


sub = 'wallstreetbets'
before = "1626101654"
after = "1626089147"
postStats = {}
postCount = 0

data = getPushShiftData(after, before, sub)
# Will run until all posts have been gathered 
# from the 'after' date up until before date
while(len(data) > 0):
    for submission in data:
        parseData(submission)
        postCount+=1
    # calls pushShiftData() with the created date of the last submission
    print(str(dt.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushShiftData(after, before, sub)

print(str(len(postStats)) + " submissions have been added to list")
print("1st entry is:")
print(list(postStats.values())[0][0][1] + " created: " + str(list(postStats.values()) [0][0][2]))
print("last entry is:")
print(list(postStats.values())[-1][0][1] + " created: " + str(list(postStats.values()) [-1][0][2]))

def subredditPost_csv():
    upload_count = 0
    location = "/homes/iws/evhuynh/summerProj2021/data/"
    print("input filename of submission file, please add .csv")
    filename = input()
    file = location + filename
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers=["Post ID", "Title", "Publish Date"]
        a.writerow(headers)
        for post in postStats:
            a.writerow(postStats[post][0])
            upload_count+=1
        print(str(upload_count) + " posts have been uploaded")

subredditPost_csv()



