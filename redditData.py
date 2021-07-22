from psaw import PushshiftAPI
import pandas as pd
import csv
import json
import requests
import string
import re
from requests.api import post
import time
import datetime as dt;

api = PushshiftAPI()

#url = 'https://api.pushshift.io/reddit/search/submission/?after=1626162766&before=1626249166&subreddit=seahawks'

def getPushShiftData(after, before, subreddit):
    url = 'https://api.pushshift.io/reddit/search/submission/?after='+str(after)+'&before='+str(before)+'&subreddit='+str(subreddit)
    print(url)
    r = requests.get(url)
    # if requests returns and error, waits and retries until valid data is returned
    while(str(r) != "<Response [200]>"):
        print("resetting requests")
        time.sleep(60)
        r = requests.get(url)

    global countRequest
    data = json.loads(r.text)
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

#checks for removed/deleted posts
def validPost(post):
    return ("link_flair_text" in post
    and post['link_flair_css_class']
    and "selftext" in post
    and post['selftext'] != "removed"
    and post['selftext'] != "[removed]"
    and post['selftext'] != "[deleted]")

def parseData(post, postStats):
    postData = list()
    # before appending posts, validates first
    if(validPost(post)):
        try:
            title = cleanText(post['title'])
        except KeyError:
            title = "NaN"
        try:
            text = cleanText(post['selftext'])
        except KeyError:
            title = "NaN"
        sub_id = post['id']
        label = 1
        created = dt.datetime.fromtimestamp(post['created_utc'])
        postData.append((sub_id, title, text, label, created))
        postStats[sub_id] = postData

def subredditPost_csv(postStats):
    upload_count = 0
    #location = "/homes/iws/evhuynh/summerProj2021/data/"
    location = ".\\data\\"
    print("input filename of submission file, please add .csv")
    filename = input()
    file = location + filename
    # writes to csv file
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers=["Post ID", "Title", "Text", "Label", "Publish Date"]
        a.writerow(headers)
        for post in postStats:
            a.writerow(postStats[post][0])
            upload_count+=1
        print(str(upload_count) + " posts have been uploaded")
    df = pd.read_csv(location + filename)
    df.drop_duplicates(subset=None, inplace=True)
    df.to_csv(location + "no_dup_" + filename, index=False)

def main():
    sub = 'wallstreetbets'
    before = "1626757785"
    after = "1626611136"
    #after = "1626264571"
    postStats = {}
    postCount = 0

    data = getPushShiftData(after, before, sub)
    # Will run until all posts have been gathered
    # from the 'after' date up until before date
    while(len(data) > 0):
        for submission in data:
            parseData(submission, postStats)
            postCount+=1
        # calls pushShiftData() with the created date of the last submission
        print(str(dt.datetime.fromtimestamp(data[-1]['created_utc'])))
        after = data[-1]['created_utc']
        data = getPushShiftData(after, before, sub)

    print(str(len(postStats)) + " submissions have been added to list")
    print("1st entry is:")
    print(list(postStats.values())[0][0][1] + " created: " + str(list(postStats.values()) [0][0][4]))
    print("last entry is:")
    print(list(postStats.values())[-1][0][1] + " created: " + str(list(postStats.values()) [-1][0][4]))
    subredditPost_csv(postStats)


if __name__ == "__main__":
    main()
