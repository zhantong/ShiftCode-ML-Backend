import numpy as np
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from os.path import basename


class Analysis:
    def run(self, input_file_path, feature_start_index, split_index):
        dataset = np.loadtxt(input_file_path, delimiter=',')
        print('file: ', basename(input_file_path))
        print('loaded data', dataset.shape)
        META = dataset[:, :feature_start_index]
        X = dataset[:, feature_start_index:-1]
        y = dataset[:, -1]
        X = preprocessing.normalize(X)
        # sc=preprocessing.StandardScaler()
        # print(X)
        # X = preprocessing.scale(X)
        print('model: ', 'Random Forest')
        X_train = X[META[:, split_index] == 1]
        X_test = X[META[:, split_index] == 0]
        y_train = y[META[:, split_index] == 1]
        y_test = y[META[:, split_index] == 0]
        print('total_input: {}'.format(len(X)))
        print('train_input: {}, test_input: {}'.format(len(X_train), len(X_test)))
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        predicted = model.predict(X_test)
        expected = y_test
        print(metrics.classification_report(expected, predicted))
        print(metrics.confusion_matrix(expected, predicted))


if __name__ == '__main__':
    analysis = Analysis()
    input_file_path = 'data_with_value.txt'
    analysis.run(input_file_path, 3, 1)
    # analysis.run(input_file_path, 4, 2)
