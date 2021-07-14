from psaw import PushshiftAPI
import pandas
import csv
import json
import requests
from requests.api import post
api = PushshiftAPI();

import datetime as dt;


#url = 'https://api.pushshift.io/reddit/search/submission/?after=1626162766&before=1626249166&subreddit=seahawks'


def getPushShiftData(after, before, subreddit):
    url = 'https://api.pushshift.io/reddit/search/submission/?after='+str(after)+'&before='+str(before)+'&subreddit='+str(subreddit)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text);
    return data['data']

def parseData(post):
    postData = list()
    title = post['title']
    url = post['url']
    try:
        flair = post['link_flair_text']
    except KeyError:
        flair= "NaN"
    author = post['author']
    sub_id = post['id']
    score = post['score']
    created = dt.datetime.fromtimestamp(post['created_utc'])
#1520561700.0
    numComms = post['num_comments']
    permalink = post['permalink']
    postData.append((sub_id,title,url,author,score,created,numComms,permalink,flair))
    postStats[sub_id] = postData


sub = 'seahawks'
before = "1626249166"
after = "1626162766"
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
    print(len(data))
    print(str(dt.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushShiftData(after, before, sub)

print(len(data))
print(str(len(postStats)) + " submissions have been added to list")
print("1st entry is:")
print(list(postStats.values())[0][0][1] + " created: " + str(list(postStats.values()) [0][0][5]))
print("last entry is:")
print(list(postStats.values())[-1][0][1] + " created: " + str(list(postStats.values()) [-1][0][5]))

def subredditPost_csv():
    upload_count = 0
    location = "\\Reddit Data\\"
    print("input filename of submission file, please add .csv")
    filename = input()
    file = location + filename
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers=["Post ID", "Title", "Url", "Author", "Score", "Publish Date", "Total No. of Comments", "Permalink", "Flair"]
        a.writerow(headers)
        for post in postStats:
            a.writerow(postStats[post][0])
            upload_count+=1
        print(str(upload_count) + " posts have been uploaded")

subredditPost_csv()



"""
start_epoch = int(dt.datetime(2021, 7, 12).timestamp())

url = 'https://api.pushshift.io/reddit/search/submission/?after=1626162766&before=1626249166&subreddit=seahawks'

print(url)
r = requests.get(url)
data = json.loads(r.text)

temp = list(api.search_submissions(
    after=start_epoch,
    subreddit='seahawks',
    filter=['url', 'author', 'title', 'subreddit'],
    #filter=['title'],
    limit=1
)) 

for i in temp:
    s = str(i);
    s = s[s.find("(")+1:s.rfind(")")]
    print(s)
    print("")
    """