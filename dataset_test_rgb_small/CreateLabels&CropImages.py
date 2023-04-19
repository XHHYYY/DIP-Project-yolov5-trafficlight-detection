import json

CROPPING = True
W = 1280
H = 720

with open('./dataset_test_rgb_small/test.json', 'r', encoding='utf8') as file:
    label_list = json.load(file)

for image in label_list:
    if image['boxes'] == []:
        continue
    else:
        for box in image['boxes']:
            x       = '{:.6f}'.format((box['x_max'] + box['x_min']) / 2 / W)
            y       = '{:.6f}'.format((box['y_max'] + box['y_min']) / 2 / H)
            width   = '{:.6f}'.format((box['x_max'] - box['x_min']) / W)
            height  = '{:.6f}'.format((box['y_max'] - box['y_min']) / H)
            label   = 9
            content = ' '.join(map(str, [label, x, y, width, height])) + '\n'
            filename = image['path'][-9:-3] + 'txt'
            with open('./dataset_test_rgb_small/labels/' + filename, 'a+') as f:
                f.write(content)
                f.close()
            
            