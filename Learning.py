import numpy as np
from sklearn.ensemble import RandomForestClassifier
import json


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
    def run(self, train_file_path, test_file_path, feature_start_index, output_file_path='predicted.txt'):
        train_dataset = np.loadtxt(train_file_path, delimiter=',')
        X_train = train_dataset[:, feature_start_index:-1]
        y_train = train_dataset[:, -1]
        test_dataset = np.loadtxt(test_file_path, delimiter=',')
        X_test = test_dataset[:, feature_start_index:]
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        predicted = model.predict(X_test)
        print('length: ', len(predicted))
        with open(output_file_path, 'w', encoding='utf-8') as fw:
            with open(test_file_path, 'r', encoding='utf-8') as fr:
                for line, value in zip(fr.readlines(), predicted):
                    fw.write(line.strip() + ',' + str(int(value)) + '\n')

    def stat(self, predicted_file_path, truth_file_path):
        truth_barcodes = None
        with open(truth_file_path, 'r', encoding='utf-8') as f:
            truth_barcodes = json.loads(f.read())['barcodeValues']
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
    learning.run('data_with_value.txt', 'data_without_value.txt', 3)
    learning.stat('predicted.txt', 'out.json')
