import re
import json


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class CleanData():
    def __init__(self):
        self.reg = re.compile(r'(.*?)\s\[(.*?)\]\s(.*?)\s(.*?)\s\[(.*?)\]\s\-\s(.*?)$')
        self.points = {}
        self.values = {}

    def load_log(self, log_file_path):
        with open(log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                res = self.reg.findall(line)
                log_type = res[0][4]
                if log_type == 'processed':
                    log_data = json.loads(res[0][5])
                    self.each_source(log_data)

    def each_source(self, data):
        samples_per_unit = data['barcode']['samplesPerUnit']

        overlap_situation = data['overlapSituation']
        is_random=data['isRandom']
        contents = list(
            chunks(data['barcode']['content'][0], samples_per_unit))
        real_points = list(
            chunks(data['barcode']['real'], samples_per_unit * 2))
        real_points = [list(chunks(points, 2))
                       for points in real_points]
        index = data['index']
        bar_1, bar_2 = self.process_varybar(data['varyBar'])
        for sample_points, content in zip(real_points, contents):
            point = sample_points[0]
            content.extend([bar_1[point[1]], bar_2[point[1]]])
            content.insert(0,overlap_situation)
            content.insert(0,1 if is_random else 0)
            content.insert(0,index)
        self.points[index] = contents
        if 'truth' in data:
            self.values[index] = data['truth']
        if is_random and 'value' in data:
            self.values[index] = data['value']
            print(index)

    def process_varybar(self, data):
        varybars = data['vary bar']
        bar_1 = self.process_varybar_single(varybars[0])
        bar_2 = self.process_varybar_single(varybars[1])
        return bar_1, bar_2

    def process_varybar_single(self, data):
        keys = data['mKeys']
        size = data['mSize']
        values = data['mValues']
        varybar = {}
        for i in range(size):
            varybar[keys[i]] = values[i]
        return varybar

    def dump_to_file(self):
        with open('data_with_value.txt', 'w', encoding='utf-8') as f_with_value \
                , open('data_without_value.txt', 'w', encoding='utf-8') as f_without_value:
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
    log_file_path = '2017-03-15 09-57-18.txt'
    barcode = CleanData()
    barcode.load_log(log_file_path)
    barcode.dump_to_file()
