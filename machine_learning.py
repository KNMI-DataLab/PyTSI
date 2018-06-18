import numpy as np
from sklearn import model_selection, neighbors
from sklearn.cluster import KMeans
import pandas as pd
from tqdm import tqdm
import settings
import matplotlib.pyplot as plt
# style.use('ggplot')


def knn():
    """K-Nearest Neighbor machine learning method. Takes the output data file as input and calculates accuarcy
    percentage of kNN using cross-validation over a large amount of iterations. Odd numbers of neighbors (m) are
    tested from 3 to 17."""
    # read input values
    df = pd.read_csv(settings.output_data)
    # replace all question marks with -99999
    df.replace('?', -99999, inplace=True)
    # drop the first column
    df.drop(['filename'], 1, inplace=True)

    # set cloud class
    X = np.array(df.drop(['cloud_type'], 1))
    y = np.array(df['cloud_type'])

    m = 3
    n = len(X)

    # loop over number of n_neighbors
    # loop over m for averaging
    # loop over LOOCV method

    for k in tqdm(range(3, 17, 2)):
        sum = 0
        for i in range(0, m):
            for j in range(0, n):
                X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=1)
                clf = neighbors.KNeighborsClassifier(n_neighbors=k, algorithm='ball_tree')
                clf.fit(X_train, y_train)
                accuracy = clf.score(X_test, y_test) * 100
                sum += accuracy
        avg = sum / (m * n)
        print('k =', k, ', LOOCV average accuracy =', avg, '%')


def k_means():
    """Implementation of the k-means machine learning algorithm. The SKLearn Python library is used used for the main
    processing and calculations. K-means clusters the n-dimensional data into n groups. Data is read from a file."""
    # read input values
    df = pd.read_csv(settings.output_data)
    # replace all question marks with -99999
    df.replace('?', -99999, inplace=True)
    # drop the first column
    df.drop(['filename'], 1, inplace=True)

    X = np.array(df.drop(['cloud_type'], 1))
    y = np.array(df['cloud_type'])

    axis1 = 0
    axis2 = 2

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(X)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    colors = ['g.', 'r.', 'c.', 'b.']

    for i in range(len(X)):
        print('True:', y[i], 'Predicted:', labels[i])

    quit()

    plt.subplot(2, 1, 1)
    plt.title('kmeans')
    # plt.scatter(X[:, axis1], X[:, axis2])
    for i in range(len(X)):
        # print('coordinate:', X[i], 'label:',labels[i])
        plt.plot(X[i, axis1], X[i, axis2], colors[labels[i]])

    plt.scatter(centroids[:, axis1], centroids[:, axis2], marker='+', s=500, linewidths=5, zorder=10, color='black')

    plt.subplot(2, 1, 2)
    plt.title('true')
    plt.scatter(X[:, axis1], X[:, axis2], c=y)
    plt.show()
