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

import nltk
from nltk.stem import WordNetLemmatizer

import sparknlp
from sparknlp.base import *
from sparknlp.common import *
from sparknlp.annotator import *
from sparknlp.training import *
from pyspark.ml import Pipeline

class visualizer_data:
     
    def __init__(self):
        self.csvName = ""

    def getPushShiftData(self, after, before, subreddit):
        print(subreddit)
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

    def cleanText(self, text):
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
    def validPost(self, post):
        return ("link_flair_text" in post
        and post['link_flair_css_class']
        and "selftext" in post
        and post['selftext'] != "removed"
        and post['selftext'] != "[removed]"
        and post['selftext'] != "[deleted]")
    
    def parseData(self, post, postStats):
        postData = list()
        # before appending posts, validates first
        if(self.validPost(post)):
            try:
                title = self.cleanText(post['title'])
            except KeyError:
                title = "NaN"
            try:
                text = self.cleanText(post['selftext'])
            except KeyError:
                title = "NaN"
            sub_id = post['id']
            label = 1
            created = dt.datetime.fromtimestamp(post['created_utc'])
            postData.append((sub_id, title, text, label, created))
            postStats[sub_id] = postData
    
    def subredditPost_csv(self, postStats):
        upload_count = 0
        location = "/homes/iws/evhuynh/summerProj2021/data/"
        #location = ".\\data\\"
        print("input filename of submission file, please add .csv")
        filename = input()
        self.csvName = filename
        file = location + filename
        # writes to csv file
        with open(file, 'w', newline='', encoding='utf-8') as file:
            a = csv.writer(file, delimiter=',')
            headers=["id", "title", "text", "label", "date"]
            a.writerow(headers)
            for post in postStats:
                a.writerow(postStats[post][0])
                upload_count+=1
            print(str(upload_count) + " posts have been uploaded")
        df = pd.read_csv(location + filename)
        df['subreddit'] = 1
        df.to_csv(location + "no_dup_" + filename, index=False)

    def main(self, subred):
        sub = subred
        sub = 'overwatch'
        before = "1626854216"
        #after = "1624262216"
        after = "1626815895"
        postStats = {}
        postCount = 0

        data = self.getPushShiftData(after, before, sub)
        # Will run until all posts have been gathered
        # from the 'after' date up until before date
        while(len(data) > 0):
            for submission in data:
                self.parseData(submission, postStats)
                postCount+=1
            # calls pushShiftData() with the created date of the last submission
            print(str(dt.datetime.fromtimestamp(data[-1]['created_utc'])))
            after = data[-1]['created_utc']
            data = self.getPushShiftData(after, before, sub)

        print(str(len(postStats)) + " submissions have been added to list")
        self.subredditPost_csv(postStats)

    if __name__ == "__main__":
        main()