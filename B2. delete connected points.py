
import os
import math


def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# def filter_close_points(points, min_distance):
#     filtered_points = []
#     for i, p1 in enumerate(points):
#         is_close = False
#         for j, p2 in enumerate(points):
#             if i != j and euclidean_distance(p1[1:], p2[1:]) < min_distance:
#                 is_close = True
#                 break
#         if not is_close:
#             filtered_points.append(p1)
#     return filtered_points

def filter_close_points(points, min_distance):
    filtered_points = []
    marked_for_removal = set()

    for i, p1 in enumerate(points):
        if i not in marked_for_removal:
            for j, p2 in enumerate(points):
                if i != j and euclidean_distance(p1[1:], p2[1:]) < min_distance:
                    marked_for_removal.add(j)

            filtered_points.append(p1)

    return filtered_points



input_folder = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\1.center txt ++9"
output_folder = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\1.center txt ++9" # Change this to your desired output folder
min_distance = 10  # Minimum distance in pixels

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, 'r') as f:
            lines = f.readlines()

        points = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 3:
                class_index = int(parts[0])
                x = float(parts[1]) * 1024
                y = float(parts[2]) * 1024
                points.append((class_index, x, y))

        filtered_points = filter_close_points(points, min_distance)

        with open(output_path, 'w') as f:
            for point in filtered_points:
                f.write(f"{point[0]} {point[1] / 1024} {point[2] / 1024}\n")

print("Processing complete.")
