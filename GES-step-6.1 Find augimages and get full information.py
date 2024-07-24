

import os
import shutil
import random

# Paths
input_txt_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\sml'
output_image_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_full_information\images'
output_label_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_full_information\labels'
image_folders = {
    's': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small',
    'm': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\middle',
    'l': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large'
}
label_folders = {
    's': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\small',
    'm': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\middle',
    'l': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\large',
    '0': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\small'
}

# Create output directories if they don't exist
os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

# Process each txt file in the input folder
for txt_file_name in os.listdir(input_txt_folder):

    txt_file_path = os.path.join(input_txt_folder, txt_file_name)

    # Check if the file is empty
    if os.path.getsize(txt_file_path) == 0:
        print(f"Skipping empty file: {txt_file_name}")
        continue
    else:
        print(f"opt file: {txt_file_name}")
        with open(txt_file_path, 'r') as txt_file:
            lines = txt_file.readlines()

        new_labels = []

        for line in lines:
            parts = line.split()
            label = parts[0]
            x = float(parts[1])
            y = float(parts[2])
            label_index_random = random.randint(1,2)
            while True:
                    image_folder = image_folders[label]
                    image_files = os.listdir(image_folder)
                    n=len(image_files)
                    random_number = random.randint(0, n-1)
                    image_filename = image_files[random_number]
                    image_path = os.path.join(image_folder, image_filename)
                    # shutil.copy(image_path, output_images_folder)
                    # Read corresponding label
                    label_filename = image_filename.replace('.png', '.txt')
                    label_file_path = os.path.join(label_folders[label], label_filename)
                    # label_file_path = os.path.join(label_folders[label], f'{os.path.splitext(txt_file_name)[0]}.txt')

                    with open(label_file_path, 'r') as label_file:
                        label_parts = label_file.readline().split()
                        label_index = label_parts[0]
                        width = float(label_parts[1])
                        height = float(label_parts[2])
                    if label_index == label_index_random:
                        continue
                    else:
                        break

            # Copy image
            image_name = f'{x} {y}.png'
            shutil.copy(os.path.join(image_folder, image_filename), os.path.join(output_image_folder, image_name))

            # Update new label
            new_label = f'{label_index} {x} {y} {width} {height}\n'
            new_labels.append(new_label)

        # Write new labels to output label file
        new_label_file_path = os.path.join(output_label_folder, txt_file_name)
        with open(new_label_file_path, 'w') as new_label_file:
            new_label_file.writelines(new_labels)



