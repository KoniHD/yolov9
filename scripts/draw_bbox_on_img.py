"""
This file takes a given bbox represented in the yolo format in a .txt file and draws it on the corresponding image.

Parameters
----------

"""
import os
import argparse
import cv2 as cv

class_names = {
    0: 'small load carrier',
    1: 'forklift',
    2: 'pallet',
    3: 'stillage',
    4: 'pallet truck'
}

def draw_bbos(dir, subset, imgName, classId):
    
    predictions = []
    labels = os.path.splitext(imgName)[0] + ".txt"
    image = cv.imread(os.path.join(dir, 'images/', subset, imgName))
    img_height, img_width = image.shape[:2]

    with open(os.path.join(dir, 'labels/', subset, labels), 'r') as f:
        for line in f:
            data = line.strip().split()
            if int(data[0]) == classId:
                predictions.append({
                    'x': float(data[1]) * img_width,
                    'y': float(data[2]) * img_height,
                    'width': float(data[3]) * img_width,
                    'height': float(data[4]) * img_height
                })

    
    for bounding_box in predictions:
        x0 = bounding_box['x'] - bounding_box['width'] / 2
        x1 = bounding_box['x'] + bounding_box['width'] / 2
        y0 = bounding_box['y'] - bounding_box['height'] / 2
        y1 = bounding_box['y'] + bounding_box['height'] / 2
    
        start_point = (int(x0), int(y0))
        end_point = (int(x1), int(y1))
        cv.rectangle(image, start_point, end_point, color=(0,255,0), thickness=2)
    
        cv.putText(
            image,
            class_names[classId],
            (int(x0), int(y1) + 20),
            fontFace = cv.FONT_HERSHEY_TRIPLEX,
            fontScale = 0.7,
            color = (255, 255, 255),
            thickness=1
        )
    if not os.path.exists(os.path.join(dir, 'bbox_anot/')):
        os.mkdir(os.path.abspath(os.path.join(dir, 'bbox_anot/')))
    cv.imwrite(os.path.join(dir, 'bbox_anot/', imgName), image)

def parse_args():
    parser = argparse.ArgumentParser()
    # for use in GitHub Codespaces use '/workspaces' as directory
    # default is the google colab directory
    parser.add_argument('--DIR', '--dir', '-d', type=str, help='Directory path to dataset folder', default='/workspace/yolov9/loco')
    parser.add_argument('--classId', '--id', '--ci', type=int, help='ID of the class to be displayed, if none is given all classes will be displayed')
    parser.add_argument('--img', type=str, help='Name of the image to be displayed')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arg = parse_args()
    if not os.path.exists(arg.DIR):
        raise FileNotFoundError(f"Directory {arg.DIR} does not exist")
    if os.path.exists(os.path.join(arg.DIR, 'images/train', arg.img)):
        draw_bbos(os.path.join(arg.DIR), 'train', arg.img, arg.classId)
    elif os.path.exists(os.path.join(arg.DIR, 'images/val', arg.img)):
        draw_bbos(os.path.join(arg.DIR), 'val', arg.img, arg.classId)
    elif os.path.exists(os.path.join(arg.DIR, 'images/test', arg.img)):
        draw_bbos(os.path.join(arg.DIR), 'val', arg.img, arg.classId)
    else:
        raise FileNotFoundError(f"Image {arg.img} does not exist")