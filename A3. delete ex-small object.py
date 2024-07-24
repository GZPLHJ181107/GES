import os

def should_remove(line):
    parts = line.strip().split()
    class_index = int(parts[0])
    x_center = float(parts[1])
    y_center = float(parts[2])
    width = float(parts[3])
    height = float(parts[4])

    # 原始图片尺寸
    image_width = 1024
    image_height = 1024

    # 转换为绝对坐标
    abs_x_center = x_center * image_width
    abs_y_center = y_center * image_height
    abs_width = width * image_width
    abs_height = height * image_height

    # 计算目标面积
    area = abs_width * abs_height

    # 返回是否应该删除目标的判断结果
    return area < 300 and class_index in [1,2]

label_folder = r"D:\GuoZhoupeng\xfbd-dataset2\random sampling + yolo-xfbd-kmeans+taoyi+smote+sml\labels\train"
output_folder = r"D:\GuoZhoupeng\xfbd-dataset2\random sampling + yolo-xfbd-kmeans+taoyi+smote+sml\labels\train"

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 遍历标签文件夹中的标签文件
for label_filename in os.listdir(label_folder):
    if label_filename.endswith('.txt'):
        label_filepath = os.path.join(label_folder, label_filename)
        output_filepath = os.path.join(output_folder, label_filename)

        with open(label_filepath, 'r') as label_file:
            lines = label_file.readlines()

        # 筛选出符合条件的目标并保存到新标签文件中
        filtered_lines = [line for line in lines if not should_remove(line)]
        with open(output_filepath, 'w') as output_file:
            output_file.writelines(filtered_lines)

        print(f"Processed {label_filename} and saved to {output_filepath}")

print("Filtering complete.")
