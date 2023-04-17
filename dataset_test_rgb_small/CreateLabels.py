import json

with open('./dataset_test_rgb_small/test.json', 'r', encoding='utf8') as file:
    ori_label_list = json.load(file)

w = 1280
h = 720

for image in ori_label_list:
    if image['boxes'] == []:
        continue
    else:
        for box in image['boxes']:
            x       = '{:.6f}'.format((box['x_max'] + box['x_min']) / 2 / w)
            y       = '{:.6f}'.format((box['y_max'] + box['y_min']) / 2 / h)
            width   = '{:.6f}'.format((box['x_max'] - box['x_min']) / w)
            height  = '{:.6f}'.format((box['y_max'] - box['y_min']) / h)
            label   = 9
            content = ' '.join(map(str, [label, x, y, width, height])) + '\n'
            filename = image['path'][-9:-3] + 'txt'
            with open('./dataset_test_rgb_small/labels/' + filename, 'a+') as f:
                f.write(content)
                f.close()
            