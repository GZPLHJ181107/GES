import os
from PIL import Image

folder_path = r"D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large"
labels_folder = r"D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\large"

def meets_condition(w, h, w1, h1):
    return abs(w - w1) < 1 and abs(h - h1) < 1

# 获取所有文件列表
file_list = os.listdir(folder_path)

for filename in file_list:
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(folder_path, filename)
        label_path = os.path.join(labels_folder, filename.replace('.jpg', '.txt').replace('.png', '.txt'))

        # 使用PIL库读取图片
        image = Image.open(image_path)
        width, height = image.size

        # 从文件名中提取w1和h1
        filename= filename.split('.p')[0]
        filename= filename.split()
        w1, h1 = float(filename[0])*1024 ,float(filename[1])*1024

        if not meets_condition(width, height, w1, h1):
            # 不满足条件，删除图片和对应的标签文件
            print(f"Removing image {filename} and its label...")
            os.remove(image_path)
            if os.path.exists(label_path):
                os.remove(label_path)
        else:
            print(f"Image {filename} meets the condition.")

        image.close()
