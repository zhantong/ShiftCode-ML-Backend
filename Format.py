import json


class Format:
    def format(self, predicted_file_path='predicted.json', meta_file_path='out.json', output_file_path='result.json'):
        predicted = None
        with open(predicted_file_path, 'r', encoding='utf-8') as f:
            predicted = json.loads(f.read())
        meta = None
        with open(meta_file_path, 'r', encoding='utf-8') as f:
            meta = json.loads(f.read())
        result = {
            'fecParameters': meta['fecParameters'],
            'values': predicted
        }
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(result))


if __name__ == '__main__':
    format = Format()
    format.format()
