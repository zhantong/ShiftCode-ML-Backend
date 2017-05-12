import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import json
from os.path import basename
from sklearn import metrics


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def find_most_common(input_list, list_of_list):
    most_common = None
    min_diff_count = 10 ** 5
    for check_list in list_of_list:
        if len(input_list) != len(check_list):
            raise Exception("length don't match", len(input_list), len(check_list))
        diff_count = len([i for i, j in zip(input_list, check_list) if i != j])
        if diff_count < min_diff_count:
            min_diff_count = diff_count
            most_common = check_list
    return min_diff_count, most_common


class Learning:
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

        with open('value.txt', 'w', encoding='utf-8') as f:
            out = predicted.astype(int).tolist()
            print(out)
            f.write(json.dumps(out))

    def run(self, train_file_path, test_file_path, feature_start_index):
        train_dataset = np.loadtxt(train_file_path, delimiter=',')
        X_train = train_dataset[:, feature_start_index:-1]
        y_train = train_dataset[:, -1]
        test_dataset = np.loadtxt(test_file_path, delimiter=',')
        X_test = test_dataset[:, feature_start_index:]
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        predicted = model.predict(X_test)
        print('length: ', len(predicted))
        with open('predicted.txt', 'w', encoding='utf-8') as fw:
            with open(test_file_path, 'r', encoding='utf-8') as fr:
                for line, value in zip(fr.readlines(), predicted):
                    fw.write(line.strip() + ',' + str(int(value)) + '\n')

    def format(self, input_file_path, output_file_path):
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

    def stat(self, predicted_file_path, truth_file_path):
        truth_barcodes = None
        with open(truth_file_path, 'r', encoding='utf-8') as f:
            truth_barcodes = json.loads(f.read())['values']
        predicted_barcodes = {}
        with open(predicted_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = list(map(int, line.strip().split(',')))
                if line[0] not in predicted_barcodes:
                    predicted_barcodes[line[0]] = []
                predicted_barcodes[line[0]].append(line[1:])
        for index in sorted(predicted_barcodes.keys()):
            predicted = [item[-1] for item in predicted_barcodes[index]]
            min_diff_count, truth = find_most_common(predicted, truth_barcodes)
            print(min_diff_count)


if __name__ == '__main__':
    input_file_path = 'data_with_value.txt'
    learning = Learning()
    # learning.run(input_file_path, 3,1)

    # learning.format('value.txt', 'value_formatted.txt')

    learning.run('data_with_value.txt', 'data_without_value.txt', 3)
    learning.stat('predicted.txt', 'out.txt')
