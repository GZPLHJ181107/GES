

import random

import os

def generate_synthetic_point(p1, p2, alpha):
    x_new = p1[0] + alpha * (p2[0] - p1[0])
    y_new = p1[1] + alpha * (p2[1] - p1[1])
    return (x_new, y_new)

def smote_oversample(points, num_samples=5, alpha=0.5):
    synthetic_points = []
    for _ in range(num_samples):
        p1 = random.choice(points)
        p2 = random.choice(points)
        synthetic_point = generate_synthetic_point(p1, p2, alpha)
        synthetic_points.append(synthetic_point)
    return synthetic_points

input_folder = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_center txt++9 smote"
output_folder = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_center txt++9 smote"  # Change this to your desired output folder

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, 'r') as f:
            lines = f.readlines()

        # Check if the file is empty, skip processing if it is
        if len(lines) == 0:
            continue

        points = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 3:
                x = float(parts[1]) * 1024
                y = float(parts[2]) * 1024
                points.append((x, y))

        synthetic_points = smote_oversample(points, num_samples=5, alpha=0.5)

        with open(output_path, 'w') as f:
            for point in points:
                f.write(f"0 {point[0] / 1024} {point[1] / 1024}\n")
            for synthetic_point in synthetic_points:
                f.write(f"0 {synthetic_point[0] / 1024} {synthetic_point[1] / 1024}\n")

print("SMOTE-based oversampling complete.")
