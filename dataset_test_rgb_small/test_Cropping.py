import json
import cv2
import os

CROPPING = True
left_list = []
cropping_flag = False
content = ''
W = 1280
H = 720
W_HALF = W / 2

with open('./dataset_test_rgb_small/test.json', 'r', encoding='utf8') as file:
    label_list = json.load(file)

for image in label_list:
    if image['boxes'] == []:
        continue
    else:
        for box in image['boxes']:
            if CROPPING:
                if box['x_min'] < W/2:
                    left_list.append(box)
                    continue
                else:
                    cropping_flag = True
                    x       = '{:.6f}'.format((box['x_max'] + box['x_min'] - 2 * W_HALF) / 2 / W_HALF)
                    y       = '{:.6f}'.format((box['y_max'] + box['y_min']) / 2 / H)
                    width   = '{:.6f}'.format((box['x_max'] - box['x_min']) / W_HALF)
                    height  = '{:.6f}'.format((box['y_max'] - box['y_min']) / H)
                    label   = 9
                    content = content + ' '.join(map(str, [label, x, y, width, height])) + '\n'

        if cropping_flag:
            r_filename = image['path'][-9:-4] + '_r.txt'
            with open('./dataset_test_rgb_small/rgb/labels/' + r_filename, 'w') as f:
                f.write(content)
                
                content = ''

        for left_box in left_list:
            x       = '{:.6f}'.format((box['x_max'] + box['x_min']) / 2 / (W_HALF if cropping_flag else W))
            y       = '{:.6f}'.format((box['y_max'] + box['y_min']) / 2 / H)
            width   = '{:.6f}'.format((box['x_max'] - box['x_min']) / (W_HALF if cropping_flag else W))
            height  = '{:.6f}'.format((box['y_max'] - box['y_min']) / H)
            label   = 9
            content = content + ' '.join(map(str, [label, x, y, width, height])) + '\n'
            
        l_filename = image['path'][-9:-4] + '_l.txt' if cropping_flag else image['path'][-9:-4] + '.txt'
        with open('./dataset_test_rgb_small/rgb/labels/' + l_filename, 'w') as f:
            f.write(content)
            
            
        if cropping_flag:
            img = cv2.imread(image['path'])
            img_l = img[:, 0:W_HALF]
            img_r = img[:, W_HALF:]
            
            os.remove(image['path'])
            cv2.imwrite(l_filename, img_l)
            cv2.imwrite(r_filename, img_r)
            
        cropping_flag = False
        
        
if __name__ == '__main__':
    
    pass
# ! next：支持输入不同的label路径和图像路径，封装为函数