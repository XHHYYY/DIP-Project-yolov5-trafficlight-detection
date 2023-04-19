from PIL import Image, ImageEnhance
import glob

TEST = False
# TEST = True

if TEST:
    temp_img = Image.open('./dataset_test_rgb_small/image_sets/white_balanced/images/24102.png')
    new = ImageEnhance.Sharpness(temp_img).enhance(5.0)
    new = ImageEnhance.Color(new).enhance(2.0)
    new.show()
else:
    path_set = glob.glob('./dataset_test_rgb_small/image_sets/white_balanced/images/*')
    for path in path_set:
        temp_img = Image.open(path)
        # new = ImageEnhance.Brightness(temp_img).enhance(2.0)
        new = ImageEnhance.Sharpness(temp_img).enhance(5.0)
        new = ImageEnhance.Color(new).enhance(2.0)
        new_path = path.replace('/white_balanced/', '/enhanced/')
        new.save(new_path)