import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

reddit_data = pd.read_csv('.\\data\\no_dup_test.csv')

features = ['title', 'text']
X = reddit_data[features]
y = reddit_data.subreddit

x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=42,
                                                    test_size=0.50)
