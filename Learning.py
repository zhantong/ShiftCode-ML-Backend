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
    def run(self, input_file_path='output.json', output_file_path='predicted.json'):
        X_train=[]
        y_train=[]
        train_indexes=[]
        with open(input_file_path,'r',encoding='utf-8') as f:
            data=json.loads(f.read())
        for frame in data['frames']:
            if frame['learningData'] and frame['barcode']['isRandom'] and 'random' in frame and 'truthValue' in frame['random']:
                X_train.extend(frame['learningData'])
                y_train.extend(frame['random']['truthValue'])
                train_indexes.append(frame['image']['index'])
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        print(model.get_params())
        test_indexes=[]
        result=[]
        for frame in data['frames']:
            if frame['learningData'] and not frame['barcode']['isRandom']:
                predicted=model.predict(frame['learningData'])
                predicted=predicted.tolist()
                result.append({
                    'index':frame['image']['index'],
                    'value':predicted
                })
                test_indexes.append(frame['image']['index'])
        data['learning']={}
        data['learning']['trainIndexes']=train_indexes
        data['learning']['testIndexes']=test_indexes
        with open(input_file_path,'w',encoding='utf-8') as f:
            f.write(json.dumps(data))
        with open(output_file_path,'w',encoding='utf-8') as f:
            f.write(json.dumps(result))

    def stat(self, predicted_file_path='predicted.json', truth_file_path='out.json'):
        truth_barcodes = None
        with open(truth_file_path, 'r', encoding='utf-8') as f:
            truth_barcodes = json.loads(f.read())['barcodeValues']
        predicted=None
        with open(predicted_file_path, 'r', encoding='utf-8') as f:
            predicted=json.loads(f.read())
        for frame in predicted:
            min_diff_count, truth = find_most_common(frame['value'], truth_barcodes)
            print(frame['index'],min_diff_count)


if __name__ == '__main__':
    learning = Learning()
    learning.run()
    learning.stat()
