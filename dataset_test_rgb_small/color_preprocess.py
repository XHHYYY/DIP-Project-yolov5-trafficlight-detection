from white_balance import white_balance
import glob
import cv2
img_path = glob.glob('./dataset_test_rgb_small/rgb/test/*')
for path in img_path:
    new_path = path.replace('/test\\', '/white_balanced_test\\')
    cv2.imwrite(new_path, white_balance(path, 4))