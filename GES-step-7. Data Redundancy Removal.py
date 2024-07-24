# -*- coding: utf-8 -*-

import os


def overlap_area(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    x_overlap = max(0, min(x1 + w1 / 2, x2 + w2 / 2) - max(x1 - w1 / 2, x2 - w2 / 2))
    y_overlap = max(0, min(y1 + h1 / 2, y2 + h2 / 2) - max(y1 - h1 / 2, y2 - h2 / 2))

    return x_overlap * y_overlap




def main():
    labels_dir = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_final_dataset_delete_occ\train"

    for label_file in os.listdir(labels_dir):
        label_file_path = os.path.join(labels_dir, label_file)
        with open(label_file_path, "r") as f:
            lines = f.readlines()
        delete_lines = []
        new_lines = []
        for line in lines:
            parts = line.split()
            class_idx = int(parts[0])
            x, y, w, h = map(float, parts[1:])
            current_box = (x, y, w, h)

            if class_idx in [1, 2]:
                for other_line in lines:
                    other_parts = other_line.split()
                    other_class_idx = int(other_parts[0])
                    if other_class_idx == 0:
                        other_x, other_y, other_w, other_h = map(float, other_parts[1:])
                        other_box = (other_x, other_y, other_w, other_h)
                        area_overlap = overlap_area(current_box, other_box)
                        if area_overlap / (other_w * other_h) >= 0.5:
                            delete_lines.append(other_line)
        for line in lines:
            if line not in delete_lines:
                new_lines.append(line)
        with open(label_file_path, "w") as f:
            f.writelines(new_lines)


if __name__ == "__main__":
    main()