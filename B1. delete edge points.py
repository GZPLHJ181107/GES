
import os
input_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\1.center txt ++9'
output_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\1.center txt ++9'

# Threshold for considering points near the image edge
EDGE_THRESHOLD = 0.003  # Adjust as needed

def point_near_edge(x, y):
    return x < EDGE_THRESHOLD or y < EDGE_THRESHOLD or x > 1 - EDGE_THRESHOLD or y > 1 - EDGE_THRESHOLD

def filter_points(file_path):
    filtered_points = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            label_index, x, y = int(parts[0]), float(parts[1]), float(parts[2])
            if not point_near_edge(x, y):
                filtered_points.append(line)
    return filtered_points

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file_name in os.listdir(input_folder):
    input_file_path = os.path.join(input_folder, file_name)
    output_file_path = os.path.join(output_folder, file_name)

    filtered_lines = filter_points(input_file_path)

    with open(output_file_path, 'w') as output_file:
        for line in filtered_lines:
            output_file.write(line)
