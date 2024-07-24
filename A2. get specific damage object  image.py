

from PIL import Image
import os

# 输入路径
image_folder = "D:/GuoZhoupeng/datasets/xfbd_yolo/train/images"
label_folder = "D:/GuoZhoupeng/datasets/xfbd_yolo/train/labels"
output_folder = r"D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)"

# 创建输出文件夹
os.makedirs(os.path.join(output_folder, "images", "small"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "images", "middle"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "images", "large"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "labels", "small"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "labels", "middle"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "labels", "large"), exist_ok=True)

# 遍历标签文件夹中的标签文件
for label_filename in os.listdir(label_folder):
    if label_filename.endswith('.txt'):
        label_filepath = os.path.join(label_folder, label_filename)
        image_filename = label_filename.replace('.txt', '.png')
        image_filepath = os.path.join(image_folder, image_filename)

        # 读取图片尺寸
        image = Image.open(image_filepath)
        image_width, image_height = image.size

        with open(label_filepath, 'r') as label_file:
            lines = label_file.readlines()

        for line in lines:
            parts = line.strip().split()
            class_index = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])

            # 转换为绝对坐标
            abs_x_center = x_center * image_width
            abs_y_center = y_center * image_height
            abs_width = width * image_width
            abs_height = height * image_height

            # 计算目标面积
            area = abs_width * abs_height

            # 筛选条件：像素面积小于300且类别索引为1或2
            if area > 300 and class_index in [1, 2]:
                x1 = int(abs_x_center - abs_width / 2)
                y1 = int(abs_y_center - abs_height / 2)
                x2 = int(abs_x_center + abs_width / 2)
                y2 = int(abs_y_center + abs_height / 2)

                # 裁剪目标并保存
                cropped_image = image.crop((x1, y1, x2, y2))
                output_image_folder = os.path.join(output_folder, "images")
                if area < 32 * 32:
                    output_image_folder = os.path.join(output_image_folder, "small")
                elif 32 * 32 <= area < 96 * 96:
                    output_image_folder = os.path.join(output_image_folder, "middle")
                else:
                    output_image_folder = os.path.join(output_image_folder, "large")

                image_new_name = f"{width} {height}.png"
                label_new_name = f"{width} {height}.txt"
                output_image_filepath = os.path.join(output_image_folder, image_new_name)
                cropped_image.save(output_image_filepath)

                # 保存标签信息
                output_label_folder = os.path.join(output_folder, "labels")
                if area < 32 * 32:
                    output_label_folder = os.path.join(output_label_folder, "small")
                elif 32 * 32 <= area < 96 * 96:
                    output_label_folder = os.path.join(output_label_folder, "middle")
                else:
                    output_label_folder = os.path.join(output_label_folder, "large")

                output_label_filepath = os.path.join(output_label_folder, label_new_name)
                with open(output_label_filepath, 'a') as label_output_file:
                    label_output_file.write(f"{class_index} {width} {height}\n")

                print(f"Cropped target from {image_filepath} and saved to {output_image_filepath}")
                print(f"Saved label info to {output_label_filepath}")

print("Cropping and label saving complete.")
