import os
import shutil
from bs4 import BeautifulSoup


def run_convert(all_data_file, all_classes, img_train, yolo_path, write_txt):
    now_path = os.getcwd()
    data_counter = 0

    for data_file in (os.listdir(all_data_file)):
        try:
            with open(data_file, 'r') as f:
                print("read file...")
                soup = BeautifulSoup(f.read(), 'xml')
                img_name = soup.select_one('filename').text
                img_w = int(soup.select_one('width').text)
                img_h = int(soup.select_one('height').text)
                img_info = []
                for obj in soup.select('object'):
                    xmin = int(obj.select_one('xmin').text)
                    xmax = int(obj.select_one('xmax').text)
                    ymin = int(obj.select_one('ymin').text)
                    ymax = int(obj.select_one('ymax').text)
                    objclass = all_classes.get(obj.select_one('name').text)

                    x = (xmin + (xmax-xmin)/2) * 1.0 / image_w
                    y = (ymin + (ymax-ymin)/2) * 1.0 / image_h
                    w = (xmax-xmin) * 1.0 / image_w
                    h = (ymax-ymin) * 1.0 / image_h
                    img_info.append(' '.join([str(objclass), str(x),str(y),str(w),str(h)]))

                # copy image to yolo path and rename
                shutil.copyfile(data_path, yolo_path + str(data_counter) + '.jpg')
                
                # create yolo bndbox txt
                with open(yolo_path + str(data_counter) + '.txt', 'a+') as f:
                    f.write('\n'.join(img_info))

                # create train or val txt
                with open(write_txt, 'a') as f:
                    path = os.path.join(now_path, yolo_path)
                    line_txt = [path + str(data_counter) + '.jpg', '\n']
                    f.writelines(line_txt)

                data_counter += 1
                    
        except Exception as e:
            print(e)
           
    print('the file is processed')


all_classes = {'class_2': 2, 'class_1': 1, 'class_0': 0}
img_train = "train/images"
yolo_path = "yolo_train/"
all_data_file = "train_bbx"
write_txt = 'cfg/train.txt'

# img_train = "val/images"
# yolo_path = "yolo_val/"
# all_data_file = "val_bbx"
# write_txt = 'cfg/val.txt'

if not os.path.exists(yolo_path):
    os.mkdir(yolo_path)

if not os.path.exists(all_data_file):
    os.mkdir(all_data_file)
    
if os.path.exists(file_info_name):
    file=open(file_info_name, 'w')
    
if os.path.exists(write_txt):
    file=open(write_txt, 'w')

run_convert(all_data_file, all_classes, img_train, yolo_path, write_txt)