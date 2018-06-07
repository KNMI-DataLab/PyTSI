import numpy as np
from sklearn import preprocessing, model_selection, neighbors
import pandas as pd
from tqdm import tqdm

df = pd.read_csv('/home/mos/Documents/TSI/machinelearning/data_tsi_256levels.csv')
df.replace(',0.0', -99999, inplace=True)
df.drop(['filename'], 1, inplace=True)

X = np.array(df.drop(['cloudClass'],1))
y = np.array(df['cloudClass'])

m=3
n=len(X)

# loop over number of n_neighbors
    # loop over m for averaging
        # loop over LOOCV method

for k in tqdm(range(3,17,2)):
    sum=0
    for i in range(0,m):
        for j in range(0,n):
            X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=1)
            clf = neighbors.KNeighborsClassifier(n_neighbors=k, algorithm='ball_tree')
            clf.fit(X_train, y_train)
            accuracy = clf.score(X_test, y_test)*100
            sum += accuracy
    avg = sum/(m*n)
    print('k =',k,', LOOCV average accuracy =',avg,'%')
