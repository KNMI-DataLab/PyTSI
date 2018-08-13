import numpy as np
from sklearn import model_selection, neighbors, svm
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
import pandas as pd
from tqdm import tqdm
import settings
import matplotlib.pyplot as plt
import itertools

def plot_accum_accur(k, accuracy, n_training, n_test):
    plt.plot(k, accuracy, label='$n_{train}$:'+str(n_training)+', $n_{test}$:'+str(n_test))

def plot_accuracies_k(k, accuracies_swim_cm, accuracies_swim_loocv, accuracies_mobotix_cm, accuracies_mobotix_loocv):
    plt.figure(figsize=(6, 4))
    ms = 6
    plt.plot(k, accuracies_swim_cm, color='tab:orange', linestyle='-', marker='x', markersize=ms, label='SWIM (CM)')
    plt.plot(k, accuracies_swim_loocv, color='tab:orange', linestyle='-', marker='o', markersize=ms, label='SWIM (LOOCV)')
    plt.plot(k, accuracies_mobotix_cm, color='tab:blue', linestyle='-', marker='x', markersize=ms, label='Mobotix (CM)')
    plt.plot(k, accuracies_mobotix_loocv, color='tab:blue', linestyle='-', marker='o', markersize=ms, label='Mobotix (LOOCV)')
    plt.legend(loc=3)
    plt.xlim(0,50)
    plt.ylim(20,100)
    plt.xlabel('k')
    plt.ylabel('k-NN accuracy (%)')
    plt.grid()
    plt.tight_layout()
    plt.savefig('/nobackup/users/mos/results/knn_accuracies_k.eps')
    plt.show()
    plt.close()

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Greys):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """

    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    #print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)

    tick_marks = np.arange(len(classes))
    plt.colorbar()
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if cm[i,j] > 0.01:
            plt.text(j, i, format(cm[i, j], fmt),
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

def knn_mobotix(k_max):
    # read csv files
    df1 = pd.read_csv(settings.project_folder + 'cloud_detection/cloudDetection/output_data/datamobotix.csv')
    df2 = pd.read_csv(settings.project_folder + 'cloud_detection/cloudDetection/output_data/cc_images.csv')

    # remove certain columns from the array
    df1.drop(df1.columns[0], axis=1, inplace=True) # file name
    df2.drop(df2.columns[[0,1,2]], axis=1, inplace=True) # index, date + time, filename

    # convert to numpy array
    data1 = np.array(df1)
    data2 = np.array(df2)

    # combine two files
    data = np.concatenate((data1,data2), axis=1)

    # delete the last column (description from Joost)
    data = np.delete(data, -1, axis=-1)

    # remove 'meerdere klasses' and 'onduidelijk' from the list
    data = data[data[:,-2]!='meerdere klasses']
    data = data[data[:, -2] != 'onduidelijk']

    # group and replace names with numbers
    # 0: 100, 1:103, 2:83, 3:130, 4:145
    # data[data == 'onbewolkt'] = 0
    # data[data == 'cirrus'] = 1
    # data[data == 'cirrocumulus'] = 1
    # data[data == 'cirrostratus'] = 1
    # data[data == 'cumulus'] = 2
    # data[data == 'altocumulus'] = 3
    # data[data == 'stratus'] = 4
    # data[data == 'altostratus'] = 4
    # data[data == 'stratocumulus'] = 4

    # 0:83, 1:102, 2:131, 3:100,  4:93, 5:53
    data[data == 'cumulus'] = 0
    data[data == 'cirrus'] = 1
    data[data == 'cirrostratus'] = 1
    data[data == 'cirrocumulus'] = 2
    data[data == 'altocumulus'] = 2
    data[data == 'onbewolkt'] = 3
    data[data == 'stratocumulus'] = 4
    data[data == 'stratus'] = 5
    data[data == 'altostratus'] = 5

    n_0 = 83
    n_1 = 102
    n_2 = 131
    n_3 = 100
    n_4 = 92
    n_5 = 53

    # give class numbers names
    class_names = ['Cumulus', 'Cirrus +\n Cirrostratus', 'Cirrocumulus +\n Altocumulus', 'Clear Sky', 'Stratocumulus', 'Stratus +\n Altostratus']

    # kNN
    # set number of training and test set
    n_training = [28]
    n_test = [25]
    n_loops = 25

    # set up figure
    plt.figure(figsize=(5, 4))

    for m in range(0,len(n_training)):
        k_list = []
        accuracy_list_cm = []
        accuracy_list_loocv = []
        for k in range(3,k_max,2):
            cnf_matrix = 0
            accuracy = 0
            # compute confusion matrix multiple times and average result
            for i in range(0, n_loops):
                # create separate arrays per class
                data_0 = data[data[:, -2] == 0] # cumulus
                data_1 = data[data[:, -2] == 1] # cirrus and cirrostratus
                data_2 = data[data[:, -2] == 2] # cirrocumulus and altocumulus
                data_3 = data[data[:, -2] == 3] # clear sky
                data_4 = data[data[:, -2] == 4] # stratocumulus
                data_5 = data[data[:, -2] == 5] # stratus and altostratus

                # separate individual arrays into separate training and test arrays
                # clear sky
                indices = np.random.choice(data_0.shape[0], size=n_training[m], replace=False)
                data_0_training_samples = data_0[indices, :]
                data_0 = np.delete(data_0, indices, axis=0)

                indices = np.random.choice(data_0.shape[0], size=n_test[m], replace=False)
                data_0_test_samples = data_0[indices, :]

                # 0
                indices = np.random.choice(data_1.shape[0], size=n_training[m], replace=False)
                data_1_training_samples = data_1[indices, :]
                data_1 = np.delete(data_1, indices, axis=0)

                indices = np.random.choice(data_1.shape[0], size=n_test[m], replace=False)
                data_1_test_samples = data_1[indices, :]

                # 1
                indices = np.random.choice(data_2.shape[0], size=n_training[m], replace=False)
                data_2_training_samples = data_2[indices, :]
                data_2 = np.delete(data_2, indices, axis=0)

                indices = np.random.choice(data_2.shape[0], size=n_test[m], replace=False)
                data_2_test_samples = data_2[indices, :]

                # 2
                indices = np.random.choice(data_3.shape[0], size=n_training[m], replace=False)
                data_3_training_samples = data_3[indices, :]
                data_3 = np.delete(data_3, indices, axis=0)

                indices = np.random.choice(data_3.shape[0], size=n_test[m], replace=False)
                data_3_test_samples = data_3[indices, :]

                # 3
                indices = np.random.choice(data_4.shape[0], size=n_training[m], replace=False)
                data_4_training_samples = data_4[indices, :]
                data_4 = np.delete(data_4, indices, axis=0)

                indices = np.random.choice(data_4.shape[0], size=n_test[m], replace=False)
                data_4_test_samples = data_4[indices, :]

                # 5
                indices = np.random.choice(data_5.shape[0], size=n_training[m], replace=False)
                data_5_training_samples = data_5[indices, :]
                data_5 = np.delete(data_5, indices, axis=0)

                indices = np.random.choice(data_5.shape[0], size=n_test[m], replace=False)
                data_5_test_samples = data_5[indices, :]

                # concatinate training set
                training_data = np.concatenate((data_0_training_samples,
                                                data_1_training_samples,
                                                data_2_training_samples,
                                                data_3_training_samples,
                                                data_4_training_samples,
                                                data_5_training_samples))

                # concatinate test set
                test_data = np.concatenate((data_0_test_samples,
                                            data_1_test_samples,
                                            data_2_test_samples,
                                            data_3_test_samples,
                                            data_4_test_samples,
                                            data_5_test_samples))

                # concatenate the training and test data to a new array
                x = np.concatenate((training_data, test_data))
                headers = 'mean_r,mean_g,mean_b,st_dev,skewness,diff_rg,diff_rb,diff_gb,energy,entropy,contrast,homogeneity,cloud,cover,class,cloud_height'
                np.savetxt('output_data/new_ml_array.csv', x, delimiter=',', header=headers)
                y = x[:, -2]
                x = np.delete(x, -2, axis=1)

                # create final test and training set
                x_train = np.delete(training_data , -2, axis=1)
                y_train = training_data[:, -2]
                x_test = np.delete(test_data , -2, axis=1)
                y_test = test_data[:, -2]

                # convert class numbers into integeres
                y_train = y_train.astype('int')
                y_test = y_test.astype('int')

                #normalize
                x_train = (x_train - x_train.min(0)) / x_train.ptp(0)
                x_test = (x_test - x_test.min(0)) / x_test.ptp(0)

                clf = neighbors.KNeighborsClassifier(n_neighbors=k, algorithm='auto', weights='uniform')
                y_pred = clf.fit(x_train, y_train).predict(x_test)
                cnf_matrix += confusion_matrix(y_test, y_pred)
                np.set_printoptions(precision=2)
                clf.fit(x_train, y_train)
                accuracy += clf.score(x_test, y_test) * 100

            # calculate averages
            cnf_matrix = cnf_matrix / (n_loops-1)
            accuracy /= (n_loops-1)

            k_list.append(k)
            accuracy_list_cm.append(accuracy)

            #print('kNN overall accuracy:', round(accuracy,3))

            y = data[:, -2]
            x = np.delete(data, -2, axis=1)

            # normalize for LOO (Leave One Out)
            x = (x - x.min(0)) / x.ptp(0)

            loo = model_selection.LeaveOneOut()
            loo.get_n_splits(x)

            counter = accuracy = 0
            for train_index, test_index in loo.split(x):
                # print(train_index, test_index)
                x_train, x_test = x[train_index], x[test_index]
                y_train, y_test = y[train_index], y[test_index]
                y_train = y_train.astype('int')
                y_test = y_test.astype('int')
                clf = neighbors.KNeighborsClassifier(n_neighbors=k, algorithm='auto')
                clf.fit(x_train, y_train)
                y_pred = clf.predict(x_test)
                accuracy += accuracy_score(y_test, y_pred) * 100
                counter += 1

            accuracy = accuracy / counter
            accuracy_list_loocv.append(accuracy)
            #print('k:', k, '| LOOCV accuracy (Mobotix):', accuracy)

        plot_accum_accur(k_list, accuracy_list_cm, n_training[m], n_test[m])
        #plot_accum_accur(k_list, accuracy_list_loocv, m)

    plt.xlim(0,50)
    plt.ylim(20,60)
    plt.grid()
    plt.xlabel('k')
    plt.ylabel('k-NN accuracy (%)')
    plt.legend(loc=3)
    #plt.show()
    #plt.savefig('/nobackup/users/mos/results/training_test_sizes_mobotix.eps')
    plt.close()

    #
    # m = 1
    # n = len(x)

    # loop over number of n_neighbors
    # loop over m for averaging
    # loop over LOOCV method

    # for k in tqdm(range(3, 17, 2)):
    #     sum = 0
    #     for i in range(0, m):
    #         for j in range(0, n):
    #             x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=1)
    #             y_train = y_train.astype('int')
    #             y_test = y_test.astype('int')
    #             #print(x_train.ptp(0))
    #             #x_train = (x_train - x_train.min(0)) / x_train.ptp(0)
    #             #x_test = (x_test - x_test.min(0)) / x_test.ptp(0)
    #             clf = neighbors.KNeighborsClassifier(n_neighbors=7, algorithm='ball_tree')
    #             clf.fit(x_train, y_train)
    #             accuracy = clf.score(x_test, y_test) * 100
    #             sum += accuracy
    #     avg = sum / (m * n)
    #     print('k =', k, ', LOOCV average accuracy =', avg, '%')

    # Plot normalized confusion matrix
    # plt.figure(figsize=(7,6))
    # plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
    #                       title='Normalized confusion matrix')
    # plt.savefig('/nobackup/users/mos/results/knn_mobotix.eps')
    # plt.show()
    # plt.close()

    return accuracy_list_cm, accuracy_list_loocv

def knn_SWIM(k_max):
    """K-Nearest Neighbor machine learning method. Takes the output data file as input and calculates accuarcy
    percentage of kNN using cross-validation over a large amount of iterations. Odd numbers of neighbors (m) are
    tested from 3 to 17."""
    # read input values
    df = pd.read_csv(settings.project_folder + 'cloud_detection/cloudDetection/output_data/dataswimcat.csv')
    # replace all question marks with -99999
    df.replace('?', -99999, inplace=True)
    # drop the first column
    df.drop(['filename'], 1, inplace=True)

    # get complete array as numpy array
    complete = np.array(df)

    class_names = ['Clear sky', 'Pattern', 'Thick white', 'Veil']

    # split each class into separate array
    n_clear_sky = 224
    n_pattern = 89
    n_thick_white = 135
    n_veil = 85

    # copy and delete 45 random rows from the individual arrays
    # copy and delete 40 random rows from the remaining individual arrays
    n_training = [45]
    n_test = [40]
    n_loops = 25

    # set up figure
    plt.figure(figsize=(5,4))

    for m in range(0, len(n_training)):
        k_list = []
        accuracy_list_cm = []
        accuracy_list_loocv = []
        for k in range(3,k_max,2):
            cnf_matrix = 0
            accuracy = 0
            for i in range(0,n_loops):
                clear_sky_data = complete[0:n_clear_sky, :]
                pattern_data = complete[n_clear_sky:n_clear_sky + n_pattern, :]
                thick_white_data = complete[n_clear_sky + n_pattern: n_clear_sky + n_pattern + n_thick_white, :]
                veil_data = complete[n_clear_sky + n_pattern + n_thick_white: n_clear_sky + n_pattern + n_thick_white + n_veil, :]

                # clear sky
                indices = np.random.choice(clear_sky_data.shape[0], size=n_training[m], replace=False)
                clear_sky_training_samples = clear_sky_data[indices, :]
                clear_sky_data = np.delete(clear_sky_data, indices, axis=0)

                indices = np.random.choice(clear_sky_data.shape[0], size=n_test[m], replace=False)
                clear_sky_test_samples = clear_sky_data[indices, :]

                # pattern
                indices = np.random.choice(pattern_data.shape[0], size=n_training[m], replace=False)
                pattern_training_samples = pattern_data[indices, :]
                pattern_data = np.delete(pattern_data, indices, axis=0)

                indices = np.random.choice(pattern_data.shape[0], size=n_test[m], replace=False)
                pattern_test_samples = pattern_data[indices, :]

                # thick white
                indices = np.random.choice(thick_white_data.shape[0], size=n_training[m], replace=False)
                thick_white_training_samples = thick_white_data[indices, :]
                thick_white_data = np.delete(thick_white_data, indices, axis=0)

                indices = np.random.choice(thick_white_data.shape[0], size=n_test[m], replace=False)
                thick_white_test_samples = thick_white_data[indices, :]

                # veil
                indices = np.random.choice(veil_data.shape[0], size=n_training[m], replace=False)
                veil_training_samples = veil_data[indices, :]
                veil_data = np.delete(veil_data, indices, axis=0)

                indices = np.random.choice(veil_data.shape[0], size=n_test[m], replace=False)
                veil_test_samples = veil_data[indices, :]

                # concatinate training set
                training_data = np.concatenate((clear_sky_training_samples,
                                                pattern_training_samples,
                                                thick_white_training_samples,
                                                veil_training_samples))

                # concatinate test set
                test_data = np.concatenate((clear_sky_test_samples,
                                                pattern_test_samples,
                                                thick_white_test_samples,
                                                veil_test_samples))

                x = np.concatenate((training_data, test_data))
                y = x[:, -1]
                x = np.delete(x, -1, axis=1)

                x_train = np.delete(training_data , -1, axis=1)
                y_train = training_data[:, -1]
                x_test = np.delete(test_data , -1, axis=1)
                y_test = test_data[:, -1]

                #normalize
                x_train = (x_train - x_train.min(0)) / x_train.ptp(0)
                x_test = (x_test - x_test.min(0)) / x_test.ptp(0)

                clf = neighbors.KNeighborsClassifier(n_neighbors=k, algorithm='auto')
                y_pred = clf.fit(x_train, y_train).predict(x_test)
                cnf_matrix += confusion_matrix(y_test, y_pred)
                np.set_printoptions(precision=2)
                clf.fit(x_train, y_train)
                accuracy += clf.score(x_test, y_test) * 100

            # calculate averages
            cnf_matrix = cnf_matrix / (n_loops-1)
            accuracy /= (n_loops-1)

            k_list.append(k)
            accuracy_list_cm.append(accuracy)

            ################################################LOOCV
            #plot_accuracies_k(k_list, accuracy_list)

            y = complete[:, -1]
            x = np.delete(complete, -1, axis=1)

            # normalize for LOO (Leave One Out)
            x = (x - x.min(0)) / x.ptp(0)

            loo = model_selection.LeaveOneOut()
            loo.get_n_splits(x)

            counter = accuracy = 0
            for train_index, test_index in loo.split(x):
                # print(train_index, test_index)
                x_train, x_test = x[train_index], x[test_index]
                y_train, y_test = y[train_index], y[test_index]
                y_train = y_train.astype('int')
                y_test = y_test.astype('int')
                clf = neighbors.KNeighborsClassifier(n_neighbors=k, algorithm='auto')
                clf.fit(x_train, y_train)
                y_pred = clf.predict(x_test)
                accuracy += accuracy_score(y_test, y_pred) * 100
                counter += 1

            accuracy = accuracy / counter
            accuracy_list_loocv.append(accuracy)
            #print('k:',k,'| LOOCV accuracy (SWIM):', accuracy)


        plot_accum_accur(k_list, accuracy_list_cm, n_training[m], n_test[m])

    plt.xlim(0,50)
    plt.ylim(60,100)
    plt.grid()
    plt.xlabel('k')
    plt.ylabel('k-NN accuracy (%)')
    plt.legend(loc=3)
    #plt.show()
    #plt.savefig('/nobackup/users/mos/results/training_test_sizes_swim.eps')
    plt.close()

    # LOOCV
    # normalize for LOO (Leave One Out)
    # x = (x - x.min(0)) / x.ptp(0)

    # training set: 45 images per class
    # test set: 40 images per class

    # m = 1
    # n = len(x)

    # loop over number of n_neighbors
    # loop over m for averaging
    # loop over LOOCV method

    # for k in tqdm(range(3, 17, 2)):
    #     sum = 0
    #     for i in range(0, m):
    #         for j in range(0, n):
    #             x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=1)
    #             clf = neighbors.KNeighborsClassifier(n_neighbors=k, algorithm='ball_tree')
    #             clf.fit(x_train, y_train)
    #             accuracy = clf.score(x_test, y_test) * 100
    #             sum += accuracy
    #     avg = sum / (m * n)
    #     print('k =', k, ', LOOCV average accuracy =', avg, '%')

    # Plot normalized confusion matrix
    # plt.figure(figsize=(7, 6))
    # plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
    #                       title='Normalized confusion matrix')
    #plt.savefig('/nobackup/users/mos/results/knn_swim.eps')
    #plt.show()
    # plt.close()

    # set cloud class
    # X = np.array(df.drop(['cloud_type'], 1))
    # y = np.array(df['cloud_type'])

    # training set: 45 images per class
    # test set: 40 images per class

    # m = 1
    # n = len(X)

    # loop over number of n_neighbors
    # loop over m for averaging
    # loop over LOOCV method

    # for k in tqdm(range(3, 17, 2)):
    #     sum = 0
    #     for i in range(0, m):
    #         for j in range(0, n):
    #             X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=1)
    #             clf = neighbors.KNeighborsClassifier(n_neighbors=k, algorithm='ball_tree')
    #             clf.fit(X_train, y_train)
    #             accuracy = clf.score(X_test, y_test) * 100
    #             sum += accuracy
    #     avg = sum / (m * n)
    #     print('k =', k, ', LOOCV average accuracy =', avg, '%')

    # X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y)
    # clf = neighbors.KNeighborsClassifier(n_neighbors=3, algorithm='ball_tree')
    # y_pred = clf.fit(X_train, y_train).predict(X_test)
    # print(y_test, y_pred)
    # cnf_matrix = confusion_matrix(y_test, y_pred)
    # np.set_printoptions(precision=2)
    # print(cnf_matrix)

    return k_list, accuracy_list_cm, accuracy_list_loocv

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

def knn():
    k_max = 50 # set to '4' to run k=3 only
    knn_accuracries_swim_cm = knn_accuracies_swim_loocv = knn_accuracies_mobotix_cm = knn_accuracies_mobotix_loocv = np.arange(2,k_max,2)
    k_list, knn_accuracries_swim_cm, knn_accuracies_swim_loocv = knn_SWIM(k_max)
    knn_accuracies_mobotix_cm, knn_accuracies_mobotix_loocv = knn_mobotix(k_max)
    plot_accuracies_k(k_list, knn_accuracries_swim_cm, knn_accuracies_swim_loocv,
                      knn_accuracies_mobotix_cm, knn_accuracies_mobotix_loocv)