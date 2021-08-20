import matplotlib.pyplot as plt
import visualizer_data as rd
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from wordcloud import WordCloud, STOPWORDS

value = input("Enter subreddit: ")

# instance of initial data collection
getData = rd.visualizer_data()
getData.main(value)
print(getData.csvName)

# reads .csv file 
reddit_data = pd.read_csv('/homes/iws/evhuynh/summerProj2021/data/' + getData.csvName)
reddit_data.drop_duplicates(subset=['title'], inplace=True)
title_words = ''
stopwords = set(STOPWORDS)

# iterates through titles and splits words and appends it
for val in reddit_data.title:
    val = str(val)
    tokens = val.split()
    title_words += " ".join(tokens) + " "

# genereates word cloud of unique words of all titles from data where size showcases frequency
wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=stopwords, min_font_size=10).generate(title_words)
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
print("Enter name of .png file: ")
plt.savefig(input())