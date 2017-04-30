import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import json
from os.path import basename
from sklearn import metrics


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

class Learning:
    def run(this,input_file_path, feature_start_index, split_index):
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

        with open('value.txt', 'w', encoding='utf-8') as f:
            out = predicted.astype(int).tolist()
            print(out)
            f.write(json.dumps(out))


    def format(this,input_file_path, output_file_path):
        raptorQ_meta = {"commonOTI": 1375211619421, "schemeSpecificOTI": 16777473}
        data = None
        with open(input_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
        data = list(chunks(data, 2500))
        out = {
            'raptorQMeta': raptorQ_meta,
            'values': data
        }
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(out))


if __name__ == '__main__':
    input_file_path='data_with_value.txt'
    learning=Learning()
    learning.run(input_file_path, 3,1)

    learning.format('value.txt', 'value_formatted.txt')
