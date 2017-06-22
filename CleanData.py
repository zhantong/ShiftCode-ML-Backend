import re
import json


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class CleanData:
    def __init__(self):
        self.reg = re.compile(r'(.*?)\s\[(.*?)\]\s(.*?)\s(.*?)\s\[(.*?)\]\s\-\s(.*?)$')
        self.points = {}
        self.values = {}

    def load_log(self, log_file_path, channels=[0]):
        with open(log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                res = self.reg.findall(line)
                log_type = res[0][4]
                if log_type == 'processed':
                    log_data = json.loads(res[0][5])
                    self.each_source(log_data, channels)

    def each_source(self, data, channels):
        index = data['image']['index']
        if 'barcode' not in data:
            print('passed image', index)
            return
        samples_per_unit = data['barcode']['samplesPerUnit']

        overlap_situation = data['barcode']['overlapSituation']
        is_random = data['barcode']['isRandom']
        contents = [list(chunks(data['barcode']['samplePixels'][channel], samples_per_unit)) for channel in channels]
        contents = [sum(item, []) for item in zip(*contents)]
        real_points = list(chunks(data['barcode']['realSampleCoordinates'], samples_per_unit * 2))
        real_points = [list(chunks(points, 2)) for points in real_points]
        packet = []
        bar_1, bar_2 = self.process_varybar(data['barcode']['varyBars'])
        for sample_points, content in zip(real_points, contents):
            current = []
            current.extend(content)
            point = sample_points[0]
            current.extend([bar_1[point[1]], bar_2[point[1]]])
            current.insert(0, overlap_situation)
            current.insert(0, 1 if is_random else 0)
            current.insert(0, index)
            packet.append(current)
        self.points[index] = packet
        if is_random and 'random' in data and 'truthValue' in data['random']:
            self.values[index] = data['random']['truthValue']
            print(index)

    def process_varybar(self, data):
        bar_1 = self.process_varybar_single(data[0])
        bar_2 = self.process_varybar_single(data[1])
        return bar_1, bar_2

    def process_varybar_single(self, data):
        keys = data['mKeys']
        size = data['mSize']
        values = data['mValues']
        varybar = {}
        for i in range(size):
            varybar[keys[i]] = values[i]
        return varybar

    def dump_to_file(self, with_class_file_path='data_with_value.txt',
                     without_class_file_path='data_without_value.txt'):
        with open(with_class_file_path, 'w', encoding='utf-8') as f_with_value \
                , open(without_class_file_path, 'w', encoding='utf-8') as f_without_value:
            for index, contents in sorted(self.points.items()):
                if index in self.values:
                    values = self.values[index]
                    for content, value in zip(contents, values):
                        content.append(value)
                        line = ','.join(str(x) for x in content)
                        f_with_value.write(line + '\n')
                else:
                    for content in contents:
                        line = ','.join(str(x) for x in content)
                        f_without_value.write(line + '\n')


if __name__ == '__main__':
    log_file_path = '2017-06-22 13-58-52.txt'
    barcode = CleanData()
    # Black White Barcode
    barcode.load_log(log_file_path, [0])
    # Color Barcode
    # barcode.load_log(log_file_path,[1,2])
    barcode.dump_to_file()
