
import os
import math
import random

def point_on_box_edge(point, box):
    comback=2
    if point is None:
        print(point)
        return "NoneType"

    x, y = point
    x_min, y_min = box[0], box[1]
    x_max, y_max = x_min + box[2], y_min + box[3]

    if abs(x - x_min)<15 or abs(x - x_max)<15:
        return "Left or Right Edge"
    elif abs(y - y_min)<15 or abs(y - y_max)<15:
        return "Top or Bottom Edge"
    else:
        return "Not on Edge"


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def symmetry_update_LR(updated_position,box):
    updated_position = list(updated_position)
    box = list(box)
    updated_position[0] = updated_position[0]+abs(box[0]-updated_position[0])
    if updated_position[0]>=1024 :
        updated_position[0]=1024
    elif updated_position[0]<=0 :
        updated_position[0]=0
    updated_position = tuple(updated_position)
    return updated_position
def symmetry_update_TB(updated_position,box):
    updated_position = list(updated_position)
    box = list(box)
    updated_position[1] = updated_position[1]+abs(box[1]-updated_position[1])
    if updated_position[1]>=1024 :
        updated_position[1]=1024
    elif updated_position[1]<=0 :
        updated_position[1]=0
    updated_position = tuple(updated_position)
    return updated_position
def is_inside_object(position, label_lines):
    add =0
    image_size =1024
    position = position.split()[1:]
    for object_position in label_lines:
        parts = object_position.split()[1:]
        object_position_list = [float(part) for part in parts]
        x_min, y_min = object_position_list[0]*image_size - 0.5 * object_position_list[2]*image_size, object_position_list[1]*image_size - 0.5 * object_position_list[3]*image_size
        x_max, y_max = object_position_list[0]*image_size + 0.5 * object_position_list[2]*image_size, object_position_list[1]*image_size + 0.5 * object_position_list[3]*image_size

        centry_x = float(position[0])*image_size
        centry_y = float(position[1])*image_size

        if x_min < centry_x < x_max and y_min < centry_y < y_max :
            add += 1
    if add > 0:
        return True
    else:
        return False

def is_inside_object_inputnochanged(position, label_lines):
    image_size =1024
    add=0
    for object_position in label_lines:
        parts = object_position.split()[1:]
        object_position_list = [float(part) for part in parts]
        x_min, y_min = object_position_list[0]*image_size - 0.5 * object_position_list[2]*image_size, object_position_list[1]*image_size - 0.5 * object_position_list[3]*image_size
        x_max, y_max = object_position_list[0]*image_size + 0.5 * object_position_list[2]*image_size, object_position_list[1]*image_size + 0.5 * object_position_list[3]*image_size

        centry_x = float(position[0])
        centry_y = float(position[1])

        if x_min < centry_x < x_max and y_min < centry_y < y_max:
            add+=1
    if add>0:
        return True
    else:
        return False
def update_position_random(original_position, target_positions, image_size):
    # 列表中的元素
    o=10
    direction = [(0, -o), (0, o), (-o, 0), (o, 0), (-o, -o), (-o, o), (o, -o), (o, o)]
    random_choice_direction = random.choice(direction)
    #列表中任选一个元素
    updated_position = (original_position[0] + random_choice_direction[0], original_position[1] + random_choice_direction[1])
    return updated_position

def update_position_correct_direction(original_position, target_positions, image_size,nearest_boxes):

    best_distance_sum = float('inf')
    best_updated_position = None
    o=10
    for dx, dy in [(0, -o), (0, o), (-o, 0), (o, 0), (-o, -o), (-o, o), (o, -o), (o, o)]:
        updated_position = (original_position[0] + dx, original_position[1] + dy)
        distance_sum = sum(distance(updated_position, target_position) for target_position in nearest_boxes)

        if distance_sum > best_distance_sum:
            best_distance_sum = distance_sum
            best_updated_position = updated_position

    return best_updated_position



def find_nearest_boxes(target_boxes, original_position, num_boxes):
    sorted_boxes = sorted(target_boxes, key=lambda box: distance((box[1], box[2]), original_position))
    return sorted_boxes[:num_boxes]

def find_largest_box(boxes):
    largest_box = max(boxes, key=lambda box: box[2] * box[3])
    return largest_box[2], largest_box[3]


input_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_center txt++9 smote_circle_run'     #center的txt
#center txt

label_folder = r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\labels\train'   #label的txt
#label txt

output_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\marked_smote_circle_run'  # Change this to the desired output folder path

image_size = (1024, 1024)  # Image size in pixels

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_folder, filename)
        label_path = os.path.join(label_folder, filename.replace('.txt', '.txt'))

        with open(input_path, 'r') as input_file, open(label_path, 'r') as label_file:
            input_lines = input_file.readlines()# list element-str '0 0.3294917887369792 0.40110337727864587'

            label_lines = [line.strip() for line in label_file.readlines() if line.strip()]# list element-str '0 0.9898390625 0.9129980468750001 0.020321875 0.0321111328125'

            target_positions = [(float(parts[1]) * image_size[0], float(parts[2]) * image_size[1]) for parts in
                                [line.split() for line in label_lines]]# list element-tuple (1013.5952, 934.9100000000001)

            updated_positions = []  # Initialize updated_positions for this input file

            for line in input_lines:

                    parts = line.strip().split()
                    original_position = (float(parts[1]) * image_size[0], float(parts[2]) * image_size[1])
                    #如果中心位置在目标框内
                    if is_inside_object(line, label_lines):
                        # 1.直接开始围绕圆圈跳点
                        label_lines_lists = [[float(value) for value in line.split()] for line in label_lines]
                        target_boxes = [(item[1] * 1024, item[2] * 1024, item[3] * 1024, item[4] * 1024) for item in
                                        label_lines_lists]  # box的信息
                        # 2.记录标签中的目标框信息

                        updated_position = update_position_random(original_position, target_positions, image_size)  # 先跳一次
                        a=0
                        while(is_inside_object_inputnochanged(updated_position,label_lines)):
                            nearest_boxes = find_nearest_boxes(target_boxes, original_position, num_boxes=3)
                            # max_dir = find_direction(nearest_boxes,updated_position)
                            # updated_position = update_position_correct_direction(original_position, target_positions,image_size,max_dir)  # 如果还在框内则进入循环再跳
                            updated_position = update_position_correct_direction(updated_position,target_positions,image_size,nearest_boxes=nearest_boxes)
                            #3.将跳圈后的位置与所有box开始匹配，如果跳到边界了则对称跳（继续跳点）
                            for box in target_boxes:

                                edge_status = point_on_box_edge(updated_position, box)
                                if edge_status == "Not on Edge":
                                    continue
                                elif edge_status =="Left or Right Edge":
                                    updated_position = symmetry_update_LR(updated_position,box)
                                elif edge_status =="Top or Bottom Edge":
                                    updated_position = symmetry_update_TB(updated_position, box)
                            print("1")
                            a+=1
                            if a>10:
                                break
                    #如果中心位置在中心框外
                    else:
                        updated_positions.append((parts[0], original_position[0] / image_size[0], original_position[1] / image_size[1]))
                    print("*********************************************")
            output_path = os.path.join(output_folder, filename)
            with open(output_path, 'w') as output_file:
                for label, x, y in updated_positions:
                    output_file.write(f"{label} {x} {y}\n")

print("Position information updated and saved.")


