import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import json


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def run(train_file, test_file):
    train_dataset = np.loadtxt(train_file, delimiter=',')
    X_train = train_dataset[:, :-1]
    y_train = train_dataset[:, -1]
    print(X_train)
    print(y_train)
    print(train_dataset.shape)
    test_dataset = np.loadtxt(test_file, delimiter=',')
    X_test = test_dataset
    print(test_dataset.shape)

    normalizer = preprocessing.Normalizer().fit(X_train)
    X_train = normalizer.transform(X_train)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    X_test = normalizer.transform(X_test)
    predicted = model.predict(X_test)
    with open('value.txt', 'w', encoding='utf-8') as f:
        out = predicted.astype(int).tolist()
        print(out)
        f.write(json.dumps(out))


def format(input_file_path, output_file_path):
    raptorQ_meta = {"commonOTI": 924240052576, "schemeSpecificOTI": 16777473}
    data = None
    with open(input_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        data = json.loads(content)
    data = list(chunks(data, 1600))
    out = {
        'raptorQMeta': raptorQ_meta,
        'values': data
    }
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(out))


if __name__ == '__main__':
    train_file = '/Users/zhantong/Desktop/ShiftBar/barCodeMachineLearn/1135/data_with_value.txt'
    test_file = '/Users/zhantong/Desktop/ShiftBar/barCodeMachineLearn/1135/data_without_value.txt'
    run(train_file, test_file)

    # format('value.txt', 'value_formatted.txt')
