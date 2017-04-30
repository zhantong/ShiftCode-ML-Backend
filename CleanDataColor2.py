from CleanData import CleanData


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class CleanDataColor2(CleanData):
    def __init__(self):
        super().__init__()

    def each_source(self, data):
        samples_per_unit = data['barcode']['samplesPerUnit']

        overlap_situation = data['overlapSituation']
        is_random = data['isRandom']
        contents = list(
            chunks(data['barcode']['content'][1], samples_per_unit))
        contents_2 = list(
            chunks(data['barcode']['content'][2], samples_per_unit))
        real_points = list(
            chunks(data['barcode']['real'], samples_per_unit * 2))
        real_points = [list(chunks(points, 2))
                       for points in real_points]
        index = data['index']

        # if is_random and index>100 and (overlap_situation==0 or overlap_situation==1):
        #     return

        bar_1, bar_2 = self.process_varybar(data['varyBar'])
        length = int(len(contents) ** 0.5)
        result = []
        for sample_points, (i_1, content), (i_2, content_2) in zip(real_points, enumerate(contents),
                                                                   enumerate(contents_2)):
            point = sample_points[0]
            current = []
            current.extend(content)
            if False:
                if i_1 >= length:
                    current.extend(contents[i_1 - length])
                else:
                    current.extend([-1] * len(content))
                if i_1 < length * (length - 1):
                    current.extend(contents[i_1 + length])
                else:
                    current.extend([-1] * len(content))
                if i_1 % length > 0:
                    current.extend(contents[i_1 - 1])
                else:
                    current.extend([-1] * len(content))
                if i_1 % length < length - 1:
                    current.extend(contents[i_1 + 1])
                else:
                    current.extend([-1] * len(content))
            current.extend(content_2)
            if False:
                if i_2 >= length:
                    current.extend(contents_2[i_2 - length])
                else:
                    current.extend([-1] * len(content_2))
                if i_2 < length * (length - 1):
                    current.extend(contents_2[i_2 + length])
                else:
                    current.extend([-1] * len(content_2))
                if i_2 % length > 0:
                    current.extend(contents_2[i_2 - 1])
                else:
                    current.extend([-1] * len(content_2))
                if i_2 % length < length - 1:
                    current.extend(contents_2[i_2 + 1])
                else:
                    current.extend([-1] * len(content_2))
            current.extend([bar_1[point[1]], bar_2[point[1]]])
            current.insert(0, overlap_situation)
            current.insert(0, 1 if is_random else 0)
            current.insert(0, index)
            result.append(current)
        self.points[index] = result
        if 'truth' in data:
            self.values[index] = data['truth']
        if is_random and 'value' in data:
            self.values[index] = data['value']
            print(index)

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
    log_file_path = 'fs_1317.txt'
    barcode = CleanDataColor2()
    barcode.load_log(log_file_path)
    barcode.dump_to_file()
