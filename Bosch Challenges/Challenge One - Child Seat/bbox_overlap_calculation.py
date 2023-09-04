import os

import pybboxes as pbx
from shapely.geometry import Polygon

W, H = 960, 640 # Images size
predicted_labels_path  = 'D:/Bosch/Challenge One - Child Seat/yolov7/runs/detect/exp/labels'
list_of_archives = os.listdir(predicted_labels_path)
print(list_of_archives)

def calculate_intersection_area(box_1, box_2):
    poly_1 = Polygon(box_1)
    poly_2 = Polygon(box_2)
    intersection_area = poly_1.intersection(poly_2).area

    return intersection_area


for archive in list_of_archives:
    if archive.endswith('.txt'):
        passager_vehicles_counts = 0
        list_of_child_seats_bbox = list()
        path = f'{predicted_labels_path}/{archive}'
        with open(path) as file:
            lines_readed = file.readlines()
            print(lines_readed)
            for line in lines_readed:
                line = line.replace('\n', '')
                print('')
                print(line)
                line_splited = line.split(' ')

                identified_class = int(line_splited[0])
                print(f'Identified_class {identified_class}')

                if identified_class == 1 and passager_vehicles_counts == 0:
                    passager_vehicles_counts += 1 # Only grabs the value for the first appearance, which should be the most confident

                    yolo_passager_vehicle_bbox = (float(line_splited[1]), float(line_splited[2]), float(line_splited[3]), float(line_splited[4]))
                    passager_vehicle_bbox_voc = pbx.convert_bbox(yolo_passager_vehicle_bbox, from_type="yolo", to_type="voc", image_size=(W, H))
                    x_min = passager_vehicle_bbox_voc[0]
                    y_max = passager_vehicle_bbox_voc[1]
                    x_max = passager_vehicle_bbox_voc[2]
                    y_min = passager_vehicle_bbox_voc[3]

                    passager_vehicle_bbox = [[x_min,y_max], [x_max,y_max], [x_max, y_min], [x_min, y_min]]
                elif identified_class == 1 and passager_vehicles_counts > 0:
                    print('Using another bounding boxes, which has a higher confidence value than this one.')
                else:
                    pass

                if identified_class == 0:
                    yolo_child_seat_bbox = (float(line_splited[1]), float(line_splited[2]), float(line_splited[3]), float(line_splited[4]))
                    child_seat_bbox_voc = pbx.convert_bbox(yolo_child_seat_bbox, from_type="yolo", to_type="voc", image_size=(W, H))
                    x_min = child_seat_bbox_voc[0]
                    y_max = child_seat_bbox_voc[1]
                    x_max = child_seat_bbox_voc[2]
                    y_min = child_seat_bbox_voc[3]
                    child_seat_bbox = [[x_min,y_max], [x_max,y_max], [x_max, y_min], [x_min, y_min]]
                    list_of_child_seats_bbox.append(child_seat_bbox)
                else:
                    pass

        print(f'List of child seats bounding boxes: {list_of_child_seats_bbox}')
        print(f'Passager car seat reference bounding boxes: {passager_vehicle_bbox}')

        for child_seat in list_of_child_seats_bbox:
            print('')
            print(f'passager: {passager_vehicle_bbox}')
            print(f'child seat: {child_seat}')
            child_seat_x_min = child_seat[0][0]
            child_seat_y_max = child_seat[0][1]
            child_seat_x_max = child_seat[2][0]
            child_seat_y_min = child_seat[2][1]
            child_seat_total_area = abs((child_seat_x_max - child_seat_x_min) * (child_seat_y_max - child_seat_y_min))
            print(f'total calculated child seat area: {child_seat_total_area}')
            intersection_calculated = calculate_intersection_area(passager_vehicle_bbox, child_seat)
            print(intersection_calculated)
            porcentage_calculated = (intersection_calculated / child_seat_total_area) * 100
            print(f'percentage of child seat inside the vehicle: {porcentage_calculated} %')
            if porcentage_calculated> 50:
                print('Child seat found the vehicle.')
            else:
                print('Child seat not found inside the vehicle.')
