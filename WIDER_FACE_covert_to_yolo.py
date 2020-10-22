import os
import shutil
import cv2

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def run_convert(data_file, wider_train, yolo_path, file_info_name, write_txt):
    now_path = os.getcwd()
    data_counter = 0

    with open(data_file, 'r') as f:
        print("read file...")
        data = f.readlines()
        
        for data_line in data:
            data_line = data_line.strip()
            data_info = data_line.split('/')

            # the image name
            if len(data_info) == 2:
                label_0_counter = 1
                data_info_path = os.path.join(data_info[0], data_info[1])
                data_path = os.path.join(wider_train, data_info_path)

                # copy image to yolo path and rename
                shutil.copyfile(data_path, yolo_path + str(data_counter) + '.jpg')
                
                image = cv2.imread(data_path)
                image_size = [image.shape[1],image.shape[0]]
                
                # image --> rename
                with open(file_info_name, 'a') as f:
                    line_txt = [data_info_path, ' --> ', yolo_path + str(data_counter) + '.jpg', '\n']
                    f.writelines(line_txt)

                with open(write_txt, 'a') as f:
                    path = os.path.join(now_path, yolo_path)
                    line_txt = [path + str(data_counter) + '.jpg', '\n']
                    f.writelines(line_txt)
                
                data_counter += 1
                label_list = []
                # process other info
                sub_count = 1
                continue

            # the count of bndBox
            if sub_count == 1:
                sub_count += 1
                continue

            # bndBox info
            print("process ", label_0_counter, " bndBox info...")
            if sub_count >= 2:
                label_0_counter += 1
                info_list = data_line.split(' ')
#                 print("WIDER FACE(x1, y1, w, h): ", info_list[0], info_list[1], info_list[2], info_list[3])
                
                xmin = int(info_list[0])
                xmax = int(info_list[0])+int(info_list[2])
                ymin = int(info_list[1])
                ymax = int(info_list[1])+int(info_list[3])
                
                box = [xmin, xmax, ymin, ymax]
                x, y, w, h = convert(image_size,box)
#                 print("YOLO txt(x, y, w, h): ", x, y, w, h)
                
                with open(yolo_path + str(data_counter-1) + '.txt', 'a+') as f:
                    f.write('0 %s %s %s %s\n' % (x, y, w, h))
                    
    print('the file is processed')


wider_train = "WIDER_train/images"
yolo_path = "yolo_train/"
data_file = "wider_face_split/wider_face_train_bbx_gt.txt"
file_info_name = 'file_info_train.txt'
write_txt = 'cfg/train.txt'

# wider_train = "WIDER_val/images"
# yolo_path = "yolo_val/"
# data_file = "wider_face_split/wider_face_val_bbx_gt.txt"
# file_info_name = 'file_info_val.txt'
# write_txt = 'cfg/val.txt'

if not os.path.exists(yolo_path):
    os.mkdir(yolo_path)
else:
    lsdir = os.listdir(yolo_path)
    for name in lsdir:
        if name.endswith('.txt') or name.endswith('.jpg'):
            os.remove(os.path.join(yolo_path, name))

if os.path.exists(file_info_name):
    file=open(file_info_name, 'w')
    
if os.path.exists(write_txt):
    file=open(write_txt, 'w')

run_convert(data_file, wider_train, yolo_path, file_info_name, write_txt)