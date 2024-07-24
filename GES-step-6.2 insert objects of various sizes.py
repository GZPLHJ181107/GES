# -*- coding: utf-8 -*-

from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import os
import cv2
from PIL import Image
def parse_label_line(line):
    values = line.split()
    x = float(values[1])
    y = float(values[2])
    return x, y




def main():
    folder_A = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_final_dataset\labels\train'
    images_folder_A =r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_final_dataset\images\train'
    folder_B = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_full_information\labels'
    images_folder_B = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_full_information\images'

    # Step 1: Iterate over label files in folder B
    for label_file_B in os.listdir(folder_B):
        if label_file_B.endswith(".txt"):
            label_path_B = os.path.join(folder_B, label_file_B)

            # Step 2: Search for corresponding image in folder A
            for label_file_A in os.listdir(folder_A):
                if os.path.splitext(label_file_A)[0] == os.path.splitext(label_file_B)[0]:
                    label_path_A = os.path.join(folder_A, label_file_A)
                    break
            #train中对应的图片的路径也找到
            image_path_A = os.path.join(images_folder_A, label_file_A.replace('.txt', '.png'))
            image_A = cv2.imread(image_path_A)

            # Extract x and y coordinates from each line in label file B
            with open(label_path_B, 'r') as f:
                for line in f:
                    #粘贴图片
                    values = line.split()
                    x, y = parse_label_line(line)
                    w, h = float(values[3])*1024,float(values[4])*1024
                    new_name = f"{x} {y}.png"
                    image_path_B = os.path.join(images_folder_B, new_name)
                    position = (int((x * 1024)-w/2), int((y * 1024)-h/2))

                    if (position[0] >= 0 and position[0] + int(w) <= image_A.shape[1] and
                            position[1] >= 0 and position[1] + int(h) <= image_A.shape[0]):
                        # Load image B using OpenCV
                        image_B = cv2.imread(image_path_B)
                        image_B = cv2.resize(image_B, (int(w), int(h)))
                        # Paste image B onto image A
                        image_A[position[1]:position[1] + image_B.shape[0],
                        position[0]:position[0] + image_B.shape[1]] = image_B
                        # #将每行line的信息插入

                        # Step 3: Insert image information into label file A
                        with open(label_path_A, 'a') as label_file_A:
                            label_file_A.write(line)
            #保存图片
            cv2.imwrite(image_path_A, image_A)
if __name__ == "__main__":
    main()




