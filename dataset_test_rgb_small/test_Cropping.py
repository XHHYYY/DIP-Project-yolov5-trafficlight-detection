import json
import cv2
import os

def ComputeParam(
    x_max, x_min, y_max, y_min, w, h,
    mode = 'whole'):
    '''
    mode = whole, left or right, tells to computer parameters of what image.
    '''
    w_half = int(w / 2)
    x       = '{:.6f}'.format((x_max + x_min - 2 * (w_half if mode=='right' else 0)) / 2 / (w if mode=='whole' else w_half))
    y       = '{:.6f}'.format((y_max + y_min) / 2 / h)
    width   = '{:.6f}'.format((x_max - x_min) / (w if mode=='whole' else w_half))
    height  = '{:.6f}'.format((y_max - y_min) / h)
    return x, y, width, height

def CreateLabelsAndCropImages(
    jsonPath = './dataset_test_rgb_small/test.json',
    label_dest = './dataset_test_rgb_small/image_sets/cropped/labels/',
    img_dest = './dataset_test_rgb_small/image_sets/cropped/images/',
    img_src = './dataset_test_rgb_small/image_sets/original/images/',
    w = 1280,
    h = 720,
    cropping = False):
    
    left_list = []
    right_flag = False
    content = ''
    img_path = ''
    w_half =int(w / 2)

    with open(jsonPath, 'r', encoding='utf8') as file:
        label_list = json.load(file)

    for image in label_list:
        if image['boxes'] == []:
            continue
        else:
            if cropping:
                for box in image['boxes']:
                    if box['x_min'] < w/2:
                        left_list.append(box)
                        continue
                    else:
                        right_flag = True
                        x, y, width, height = ComputeParam(
                            box['x_max'], box['x_min'], box['y_max'], box['y_min'], w, h, mode='right')
                        label = 9
                        content = content + ' '.join(map(str, [label, x, y, width, height])) + '\n'

                if right_flag:
                    r_filename = image['path'][-9:-4] + '_r.txt'
                    with open(label_dest + r_filename, 'w') as f:
                        f.write(content)
                        content = ''

                for left_box in left_list:
                    left_flag = True
                    x, y, width, height = ComputeParam(
                        left_box['x_max'], left_box['x_min'], left_box['y_max'], left_box['y_min'], w, h, mode='left')
                    label = 9
                    content = content + ' '.join(map(str, [label, x, y, width, height])) + '\n'
                    
                if left_flag:
                    l_filename = image['path'][-9:-4] + '_l.txt'
                    with open(label_dest + l_filename, 'w') as f:
                        f.write(content)
                        content = ''
                    
                img_path = img_src + image['path'][-9:]
                img = cv2.imread(img_path)
                if left_flag:
                    img_l = img[:, 0:w_half, :]
                    cv2.imwrite(img_dest + l_filename.replace('txt', 'png'), img_l)
                
                if right_flag:
                    img_r = img[:, w_half:, :]
                    cv2.imwrite(img_dest + r_filename.replace('txt', 'png'), img_r)


                right_flag  = False
                left_flag   = False
                left_list   = []
                content     = ''
                
            else:
                for box in image['boxes']:
                    x, y, width, height = ComputeParam(
                        box['x_max'], box['x_min'], box['y_max'], box['y_min'], w, h, mode='whole')
                    label   = 9
                    content = ' '.join(map(str, [label, x, y, width, height])) + '\n'
                filename = image['path'][-9:-3] + 'txt'
                with open('./dataset_test_rgb_small/labels/' + filename, 'a+') as f:
                    f.write(content)
                    content = ''
        
if __name__ == '__main__':
    CreateLabelsAndCropImages(cropping=True)
# ! next：支持输入不同的label路径和图像路径，封装为函数