

import os
import math

# Define constants
# s1 = 16
# s2 = 16 * math.sqrt(2)
# s3 = 48 * math.sqrt(2)
s1 = 1
s2 = 8
s3 = 12

# Function to check if a point lies within a rectangle
def find_nearest_boxes(target_boxes, original_position, num_boxes):
    sorted_boxes = sorted(target_boxes, key=lambda box: p_distance((box[1], box[2]), original_position))
    return sorted_boxes[:num_boxes]
def p_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)




def circle_intersects_rect_easy(circle, labels,point):
    label_lines_lists = [[float(value) for value in line.split()] for line in labels]
    labels = [(item[1] , item[2] , item[3] , item[4] ) for item in
                    label_lines_lists]  # box的信息
    nearest_boxes = find_nearest_boxes(labels,point,num_boxes=3)
    sum = 0
    for box in nearest_boxes:
        x1, y1, width, height = box[0],box[1],box[2],box[3]
        rect = (x1, y1, width, height)
        circle_x, circle_y, circle_radius = circle
        circle_o =(circle_x,circle_y)
        rect_cx, rect_cy, rect_w, rect_h = rect
        rect_x1 = rect_cx-rect_w/2#左边
        rect_x2 = rect_cx+rect_w/2#右边
        rect_y1 = rect_cy-rect_h/2#上边
        rect_y2 = rect_cy+rect_h/2#下边
        rect_x1_y1 =(rect_x1,rect_y1)
        #左上角
        rect_x2_y1 =(rect_x2,rect_y1)
        #右上角
        rect_x1_y2 =(rect_x1,rect_y2)
        #左下角
        rect_x2_y2 =(rect_x2,rect_y2)
        #右下角
        circle_radius = circle_radius/1024
        co_to_linex1_y1_x2_y1 = abs(circle_y-rect_y1)
        #到上边的距离

        co_to_linex1_y2_x2_y2 = abs(circle_y-rect_y2)
        #到下边的距离

        co_to_linex1_y1_x1_y2 = abs(circle_x-rect_x1)
        #到左边的距离

        co_to_linex2_y1_x2_y2 = abs(circle_y-rect_x2)
        #到右边的距离


        if p_distance(circle_o,rect_x1_y1)<circle_radius or p_distance(circle_o,rect_x2_y1)<circle_radius or p_distance(circle_o,rect_x1_y2)<circle_radius or p_distance(circle_o,rect_x2_y2)<circle_radius :
            sum +=1
        elif co_to_linex1_y1_x2_y1<circle_radius or co_to_linex1_y2_x2_y2<circle_radius or co_to_linex1_y1_x1_y2<circle_radius or co_to_linex2_y1_x2_y2<circle_radius:
            sum +=1
    if sum>0:
        #存在相交则返回True
        return True
    else:
        #不存在相交则返回False
        return False




def circle_intersects_rect(circle, labels):
    sum = 0
    for label in labels:
        class_idx, x1, y1, width, height = map(float, label.strip().split())
        rect = (x1, y1, width, height)
        circle_x, circle_y, circle_radius = circle
        circle_o =(circle_x,circle_y)
        rect_cx, rect_cy, rect_w, rect_h = rect
        rect_x1 = rect_cx-rect_w/2#左边
        rect_x2 = rect_cx+rect_w/2#右边
        rect_y1 = rect_cy-rect_h/2#上边
        rect_y2 = rect_cy+rect_h/2#下边
        rect_x1_y1 =(rect_x1,rect_y1)
        #左上角
        rect_x2_y1 =(rect_x2,rect_y1)
        #右上角
        rect_x1_y2 =(rect_x1,rect_y2)
        #左下角
        rect_x2_y2 =(rect_x2,rect_y2)
        #右下角
        circle_radius = circle_radius/1024
        co_to_linex1_y1_x2_y1 = abs(circle_y-rect_y1)
        #到上边的距离

        co_to_linex1_y2_x2_y2 = abs(circle_y-rect_y2)
        #到下边的距离

        co_to_linex1_y1_x1_y2 = abs(circle_x-rect_x1)
        #到左边的距离

        co_to_linex2_y1_x2_y2 = abs(circle_x-rect_x2)
        #到右边的距离

        top_left= co_to_linex1_y1_x2_y1<circle_radius and co_to_linex1_y1_x2_y1< circle_radius
        #到上左边的距离均小于半径则一定相交

        top_right= co_to_linex1_y1_x2_y1<circle_radius and co_to_linex2_y1_x2_y2<circle_radius
        #到上右边的距离均小于半径则一定相交

        bottom_left = co_to_linex1_y2_x2_y2<circle_radius and co_to_linex1_y1_x1_y2<circle_radius
        #到下左边的距离均小于半径则一定相交

        bottom_right = co_to_linex1_y2_x2_y2<circle_radius and co_to_linex2_y1_x2_y2<circle_radius
        #到下右边的距离均小于半径则一定相交

        if p_distance(circle_o,rect_x1_y1)<circle_radius or p_distance(circle_o,rect_x2_y1)<circle_radius or p_distance(circle_o,rect_x1_y2)<circle_radius or p_distance(circle_o,rect_x2_y2)<circle_radius :
            sum +=1
        elif top_right or top_left or bottom_left or bottom_right:
            sum +=1
    if sum>0:
        #存在相交则返回True
        return True
    else:
        #不存在相交则返回False
        return False



folder_a = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\sml"
folder_b = r"D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\labels\train"

for filename in os.listdir(folder_a):
    if filename.endswith(".txt"):
        with open(os.path.join(folder_a, filename), 'r') as file:
            points = file.readlines()
        updated_points = []
        label_filename = os.path.join(folder_b, filename)
        if os.path.exists(label_filename):
            with open(label_filename, 'r') as label_file:
                labels = label_file.readlines()

            for point in points:
                _, x, y = map(float, point.strip().split())
                circle1 = (x, y, s1)
                circle2 = (x, y, s2)
                circle3 = (x, y, s3)
                point_position=(x,y)
                lm =True
                l=True

                if circle_intersects_rect(circle=circle1, labels=labels):
                    delete_point = True
                    #最小的16的圆有相交则删除此点，不将词典更新到新位置的列表
                    #之后再判断对于16*1.412的圆是否相交
                elif circle_intersects_rect(circle=circle2,labels=labels):
                    #与16的圆不相交，与16*1.412的圆相交则认定可以放小目标
                    updated_point = 's' + point[1:]
                    updated_points.append(updated_point)
                    lm= False#这个是停止此循环的标志位，如果这个代码执行了，那么下一个判断结果就要依照此次执行的代码来决定是否执行
                elif circle_intersects_rect(circle=circle3, labels=labels) or lm:#只有42*1.412的圆与rect相交且lm标志位没有变仍未True时才执行以下代码
                    updated_point = 'm' + point[1:]
                    updated_points.append(updated_point)
                    l = False
                    #当执行了这些代码时l变成False防止再执行最后的代码。防止把m又变成了l

                elif l :
                    #如果都没变上一个代码执行了那么l变为False就不执行下面这个代码了，但是如果上面那个没执行那么l仍旧是True则执行下面的代码
                    updated_point = 'l' + point[1:]
                    updated_points.append(updated_point)

        # Write back the modified points to the file
        with open(os.path.join(folder_a, filename), 'w') as file:
            file.writelines(updated_points)

