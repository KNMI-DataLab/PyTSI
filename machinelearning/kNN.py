import numpy as np
from sklearn import preprocessing, model_selection, neighbors
from sklearn.model_selection import LeaveOneOut
import pandas as pd
import sys

df = pd.read_csv('/home/mos/Documents/TSI/machinelearning/data_tsi_32levels.csv')
df.replace(',0.0', -99999, inplace=True)
df.drop(['filename'], 1, inplace=True)

X = np.array(df.drop(['cloudClass'],1))
y = np.array(df['cloudClass'])

X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.1)

clf = neighbors.KNeighborsClassifier(n_neighbors=9)
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)
print(accuracy)
