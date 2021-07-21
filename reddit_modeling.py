import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split

reddit_data = pd.read_csv('.\\data\\cleanedWSB_data.csv')

features = ['Title']
x = reddit_data[features]
y = reddit_data.subreddit

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42,
                                                    test_size=0.50, stratify=y)
print(reddit_data)