import numpy as np
from sklearn import preprocessing
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from os.path import basename

modes = [
    {
        'train_size': 1,
        'test_all': True
    },
    {
        'train_size': 0.3,
        'test_all': False
    },
    {
        'train_size': 0.2,
        'test_all': False
    },
    {
        'train_size': 0.1,
        'test_all': False
    },
    {
        'train_size': 0.05,
        'test_all': False
    }
]


def train_test_split(X, y, train_size, test_all=False):
    num_rows, num_columns = X.shape
    num_train = (int)(num_rows * train_size)
    if test_all:
        return X[:num_train], X, y[:num_train], y
    else:
        return X[:num_train], X[num_train:], y[:num_train], y[num_train:]


def run(input_file_path):
    dataset = np.loadtxt(
        input_file_path, delimiter=',')
    print(dataset.shape)
    X = dataset[:, 0:7]
    y = dataset[:, 7]
    # print(X)
    # print(y)
    X = preprocessing.normalize(X)
    # sc=preprocessing.StandardScaler()
    # print(X)
    # X = preprocessing.scale(X)
    print('file: ', basename(input_file_path))
    print('model: ', 'Random Forest')
    print('*' * 40)
    for mode in modes:
        param_train_size = mode['train_size']
        param_test_all = mode['test_all']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, param_train_size, param_test_all)
        print('train_pct: {}, total_num: {}'.format(param_train_size, len(X)))
        print('train_num: {}, test_num: {}'.format(len(X_train), len(X_test)))
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        predicted = model.predict(X_test)
        expected = y_test
        print(metrics.classification_report(expected, predicted))
        print(metrics.confusion_matrix(expected, predicted))
        print('-' * 40)


if __name__ == '__main__':
    files = [
        'data_with_value.txt'
    ]
    for file_path in files:
        run(file_path)
