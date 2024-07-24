import os


points_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\1.center txt ++9'
labels_folder = r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\labels\train'

output_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\1.center txt ++9'

def point_inside_box(point, box):
    x, y = point
    x_mid, y_mid, width, height = box
    return x_mid-width/2 <= x <= x_mid + width/2 and y_mid-height/2 <= y <= y_mid + height/2

def process_txt_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            label_index, x, y = int(parts[0]), float(parts[1]), float(parts[2])
            data.append((x, y))
    return data

def process_labels_file(file_path):
    boxes = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            label_index, x, y, width, height = int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
            boxes.append((x, y, width, height))
    return boxes

def filter_points_with_labels(points, labels):
    filtered_points = []
    for point in points:
        point_inside_any_box = False
        for box in labels:
            if point_inside_box(point, box):
                point_inside_any_box = True
                break
        if not point_inside_any_box:
            filtered_points.append(point)
    return filtered_points

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file_name in os.listdir(points_folder):
    points_file_path = os.path.join(points_folder, file_name)
    labels_file_path = os.path.join(labels_folder, file_name)
    output_file_path = os.path.join(output_folder, file_name)

    points = process_txt_file(points_file_path)
    labels = process_labels_file(labels_file_path)

    filtered_points = filter_points_with_labels(points, labels)

    with open(output_file_path, 'w') as output_file:
        for point in filtered_points:
            output_file.write(f"0 {point[0]} {point[1]}\n")
