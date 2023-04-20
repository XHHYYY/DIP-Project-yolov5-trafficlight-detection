from PIL import Image, ImageEnhance
import glob

TEST = False
# TEST = True

BRIGHTNESS  = 1
SHARPNESS   = 1
CONTRAST    = 1
COLOR       = 2

src = 'original'
dest = 'enhanced'
src_path = './dataset_test_rgb_small/image_sets/' + src + '/images/'
path_set = glob.glob(src_path + '*') if not TEST else [src_path + '37024.png']

for path in path_set:
    temp_img = Image.open(path)
    new = temp_img

    new = ImageEnhance.Brightness   (new).enhance(BRIGHTNESS)
    new = ImageEnhance.Sharpness    (new).enhance(SHARPNESS)
    new = ImageEnhance.Contrast     (new).enhance(CONTRAST)
    new = ImageEnhance.Color        (new).enhance(COLOR)
    new_path = path.replace(src, dest)
    if not TEST:
        new.save(new_path)
    else:
        new.show()

if not TEST:
    with open('./dataset_test_rgb_small/image_sets/' + dest + '/info.txt', 'w') as f:
        f.write(f'imgsrc: {src}\nBrightness: {BRIGHTNESS}\nSHARPNESS: {SHARPNESS}\nCONTRAST: {CONTRAST}\nCOLOR: {COLOR}')
