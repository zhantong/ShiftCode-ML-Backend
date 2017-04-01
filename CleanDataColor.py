from CleanData import CleanData


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class CleanDataColor(CleanData):
    def __init__(self):
        super(CleanData, self).__init__()

    def each_source(self, data):
        samples_per_unit = data['barcode']['samplesPerUnit']

        overlap_situation = data['overlapSituation']
        is_random = data['isRandom']
        contents_1 = list(
            chunks(data['barcode']['content'][1], samples_per_unit))
        contents_2 = list(
            chunks(data['barcode']['content'][2], samples_per_unit))
        real_points = list(
            chunks(data['barcode']['real'], samples_per_unit * 2))
        real_points = [list(chunks(points, 2))
                       for points in real_points]
        index = data['index']
        bar_1, bar_2 = self.process_varybar(data['varyBar'])
        length = int(len(contents_1) ** 0.5)
        result_1 = []
        result_2 = []
        for sample_points, (i_1, content_1), (i_2, content_2) in zip(real_points, enumerate(contents_1),
                                                                     enumerate(contents_2)):
            current_1 = []
            current_1.extend(content_1)
            point = sample_points[0]
            if i_1 >= length:
                current_1.extend(contents_1[i_1 - length])
            else:
                current_1.extend([-1] * len(content_1))
            if i_1 < length * (length - 1):
                current_1.extend(contents_1[i_1 + length])
            else:
                current_1.extend([-1] * len(content_1))
            if i_1 % length > 0:
                current_1.extend(contents_1[i_1 - 1])
            else:
                current_1.extend([-1] * len(content_1))
            if i_1 % length < length - 1:
                current_1.extend(contents_1[i_1 + 1])
            else:
                current_1.extend([-1] * len(content_1))
            current_1.extend([bar_1[point[1]], bar_2[point[1]]])
            current_1.insert(0, overlap_situation)
            current_1.insert(0, 1 if is_random else 0)
            current_1.insert(0, index)

            current_2 = []
            current_2.extend(content_2)
            if i_2 >= length:
                current_2.extend(contents_2[i_2 - length])
            else:
                current_2.extend([-1] * len(content_2))
            if i_2 < length * (length - 1):
                current_2.extend(contents_2[i_2 + length])
            else:
                current_2.extend([-1] * len(content_2))
            if i_2 % length > 0:
                current_2.extend(contents_2[i_2 - 1])
            else:
                current_2.extend([-1] * len(content_2))
            if i_2 % length < length - 1:
                current_2.extend(contents_2[i_2 + 1])
            else:
                current_2.extend([-1] * len(content_2))
            current_2.extend([bar_1[point[1]], bar_2[point[1]]])
            current_2.insert(0, overlap_situation)
            current_2.insert(0, 1 if is_random else 0)
            current_2.insert(0, index)

            current_1.insert(0, 1)
            current_2.insert(0, 2)
            result_1.append(current_1)
            result_2.append(current_2)
        self.points[index] = (result_1, result_2)
        if 'truth' in data:
            self.values[index] = data['truth']
        if is_random and 'value' in data:
            self.values[index] = data['value']
            print(index)

    def dump_to_file(self):
        with open('data_with_value.txt', 'w', encoding='utf-8') as f_with_value \
                , open('data_without_value.txt', 'w', encoding='utf-8') as f_without_value:
            for index, (contents_1, contents_2) in sorted(self.points.items()):
                if index in self.values:
                    values = self.values[index]
                    for content_1, content_2, value in zip(contents_1, contents_2, values):
                        content_1.append(value >> 2)
                        line = ','.join(str(x) for x in content_1)
                        f_with_value.write(line + '\n')
                        content_2.append(value & 0x3)
                        line = ','.join(str(x) for x in content_2)
                        f_with_value.write(line + '\n')
                else:
                    for content_1, content_2 in zip(contents_1, contents_2):
                        line = ','.join(str(x) for x in content_1)
                        f_without_value.write(line + '\n')
                        line = ','.join(str(x) for x in content_2)
                        f_without_value.write(line + '\n')


if __name__ == '__main__':
    log_file_path = '2017-03-20 18-53-43.txt'
    barcode = CleanDataColor()
    barcode.load_log(log_file_path)
    barcode.dump_to_file()
