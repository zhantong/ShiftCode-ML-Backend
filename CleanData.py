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

    def format_log(self, log_file_path, channels=(0,), output_file_path='output.json'):
        log_reg = re.compile(r'(.*?)\s\[(.*?)\]\s(.*?)\s(.*?)\s\[(.*?)\]\s\-\s(.*?)$')
        result = {}
        result['frames'] = []
        result['file'] = {}
        with open(log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                res = log_reg.findall(line)
                log_type = res[0][4]
                log_content = res[0][5]
                if log_type == 'source':
                    result['file']['path'] = log_content
                elif log_type == 'barcodeConfig':
                    result['barcodeConfig'] = json.loads(log_content)
                elif log_type == 'processed':
                    log_content = json.loads(log_content)
                    log_content['learningData'] = self.each_source(log_content, channels)
                    result['frames'].append(log_content)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(result))

    def each_source(self, data, channels):
        if 'barcode' not in data:
            return []
        samples_per_unit = data['barcode']['samplesPerUnit']

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
            packet.append(current)
        return packet

    def process_varybar(self, data):
        bar_1 = self.process_varybar_single(data[0])
        bar_2 = self.process_varybar_single(data[1])
        return bar_1, bar_2

    def process_varybar_single(self, data):
        varybar = {}
        for key, value in data['map'].items():
            varybar[int(key)] = value
        return varybar


if __name__ == '__main__':
    log_file_path = '/Volumes/扩展存储/MegaLight附加实验/拍摄到视频/小米mix2/100/VID_20180913_160548/Screen-Camera/2018-10-23-23-24-01.log'
    barcode = CleanData()
    # Black White Barcode
    barcode.format_log(log_file_path, (0,))
    # Color Barcode
    # barcode.load_log(log_file_path,(1,2))
