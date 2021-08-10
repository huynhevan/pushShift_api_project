import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from wordcloud import WordCloud, STOPWORDS

# reads .csv file 
reddit_data = pd.read_csv('/homes/iws/evhuynh/summerProj2021/data/overwatch.csv')
print(reddit_data.__len__)
reddit_data.drop_duplicates(subset=['Title'], inplace=True)
print(reddit_data.__len__)

title_words = ''
stopwords = set(STOPWORDS)
# iterates through titles and splits words and appends it
for val in reddit_data.Title:
    val = str(val)
    tokens = val.split()
    title_words += " ".join(tokens) + " "

# genereates word cloud of unique words of all titles from data where size showcases frequency
wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=stopwords, min_font_size=10).generate(title_words)
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.savefig('test.png')