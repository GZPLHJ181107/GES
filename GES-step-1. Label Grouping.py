import os
import numpy as np
from sklearn.cluster import KMeans

# Path to the dataset and labels
image_folder = r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\images\train'
label_folder = r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\labels\train'
output_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\center txt9'  # Change this to the desired output folder


def parse_yolo_label(label_path):
    with open(label_path, 'r') as f:
        lines = f.readlines()
    labels = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 5:
            label_idx = int(parts[0])
            if label_idx == 0:  # Considering only label index 0
                x_center = float(parts[1])
                y_center = float(parts[2])
                labels.append([x_center, y_center])
    return np.array(labels)


def kmeans_clustering(points, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters,n_init=10, random_state=0)
    kmeans.fit(points)
    centers = kmeans.cluster_centers_
    return centers


def write_centers_to_txt(centers, output_path):
    with open(output_path, 'w') as f:
        for center in centers:
            line = f"0 {center[0]} {center[1]}\n"
            f.write(line)




# ... (之前的代码保持不变)


# ... （之前的代码不变）

# Process each image and its corresponding label
for image_name in os.listdir(image_folder):
    image_path = os.path.join(image_folder, image_name)
    label_name = image_name.replace('.png', '.txt')
    label_path = os.path.join(label_folder, label_name)

    if os.path.exists(label_path):
        labels = parse_yolo_label(label_path)

        if len(labels) > 3:  # Only use K-means if there are more than 3 labels
            # Calculate the number of clusters for K-means based on label count
            # n_clusters = max(len(labels) // 3, 1)
            # n_clusters = min(n_clusters, 15)

            n_clusters = max(len(labels) // 3, 1)
            n_clusters = min(n_clusters, 9)


            # Perform K-means clustering
            centers = kmeans_clustering(labels, n_clusters)

            # Write cluster centers to output txt file
            output_txt_path = os.path.join(output_folder, f'{os.path.splitext(image_name)[0]}.txt')
            write_centers_to_txt(centers, output_txt_path)
        else:
            # If there are 3 or fewer labels, simply use the label coordinates as the "center"
            centers = labels

            # Write label coordinates to output txt file
            output_txt_path = os.path.join(output_folder, f'{os.path.splitext(image_name)[0]}.txt')
            write_centers_to_txt(centers, output_txt_path)

print("Clustering and txt generation completed.")


