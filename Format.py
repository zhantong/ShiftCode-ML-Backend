import json


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class Format:
    def format(self, predicted_file_path, meta_file_path, output_file_path='result.json'):
        contet = None
        with open(predicted_file_path, 'r', encoding='utf-8') as f:
            content = [int(line.strip().rsplit(',', 1)[-1]) for line in f]
        meta = None
        with open(meta_file_path, 'r', encoding='utf-8') as f:
            meta = json.loads(f.read())
        size_chunk = meta['barcodeConfig']['mainWidth'] * meta['barcodeConfig']['mainHeight']
        chunked_content = list(chunks(content, size_chunk))
        result = {
            'FECParameters': meta['FECParameters'],
            'values': chunked_content
        }
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(result))


if __name__ == '__main__':
    format = Format()
    format.format('predicted.txt', 'out.json')
