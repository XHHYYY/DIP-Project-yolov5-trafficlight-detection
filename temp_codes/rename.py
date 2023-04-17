import glob
import os
names = glob.glob('./dataset_test_rgb_small/rgb/test/*')
for counter, obj in enumerate(names):
    new_name = './dataset_test_rgb_small/rgb/test/' + str(counter) + '.png'
    os.rename(obj, new_name)