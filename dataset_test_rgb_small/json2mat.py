import json
from scipy.io import savemat

'''
将json文件的信息输出至positions.mat用于进一步分析
'''

jsonPath = './dataset_test_rgb_small/test.json'
with open(jsonPath, 'r', encoding='utf8') as file:
        label_list = json.load(file)

x_max = []
x_min = []
y_max = []
y_min = []

for image in label_list:
    if image['boxes'] == []:
        continue
    else:
        for box in image['boxes']:
            x_max.append(box['x_max'])
            x_min.append(box['x_min'])
            y_max.append(box['y_max'])
            y_min.append(box['y_min'])

filename = './matlab_process/positions.mat'
savemat(filename, {'x_max':x_max, 'x_min':x_min, 'y_max':y_max, 'y_min':y_min})