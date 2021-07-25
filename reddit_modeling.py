import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

reddit_data = pd.read_csv('.\\data\\oneMonth_WSB_data.csv')

features = ['Title', 'Text']
X = reddit_data[features]
y = reddit_data.subreddit

x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=42,
                                                    test_size=0.50)

clf = SVC(kernal='linear', C=3)
clf.fit(x_train, y_train)

clf2 = DecisionTreeClassifier()
clf2.fit(x_train, y_train)

clf3 = RandomForestClassifier()
clf3.fit(x_train, y_train)

print(f'SVC : {clf.score(x_test, y_test)}')
print(f'DTC : {clf2.score(x_test, y_test)}')
print(f'RFC : {clf3.score(x_test, y_test)}')
