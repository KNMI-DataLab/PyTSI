import numpy as np
from sklearn import model_selection, neighbors
import pandas as pd

df = pd.read_csv('/home/mos/Documents/TSI/machinelearning/data_tsi_256levels.csv')
df.replace(',0.0', -99999, inplace=True)
df.drop(['filename'], 1, inplace=True)

X = np.array(df.drop(['cloudClass'], 1))
y = np.array(df['cloudClass'])

k = 3

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=1)
clf = neighbors.KNeighborsClassifier(n_neighbors=k, algorithm='ball_tree')
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test) * 100
print(accuracy)
