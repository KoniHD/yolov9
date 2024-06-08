"""
This file takes a given bbox represented in the yolo format in a .txt file and draws it on the corresponding image.

Parameters
----------

"""
import os
import argparse
import cv2

def draw_bbos(dir, subset, img):
    for bounding_box in predictions['predictions']:
        x0 = bounding_box['x'] - bounding_box['width'] / 2
        x1 = bounding_box['x'] + bounding_box['width'] / 2
        y0 = bounding_box['y'] - bounding_box['height'] / 2
        y1 = bounding_box['y'] + bounding_box['height'] / 2
    
        start_point = (int(x0), int(y0))
        end_point = (int(x1), int(y1))
        cv2.rectangle(img, start_point, end_point, color=(0,0,0), thickness=1)
    
        cv2.putText(
            image,
            bounding_box["class"],
            (int(x0), int(y0) - 10),
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale = 0.6,
            color = (255, 255, 255),
            thickness=2
    )
    cv2.imwrite("example_with_bounding_boxes.jpg", image)

def parse_args():
    parser = argparse.ArgumentParser()
    # for use in GitHub Codespaces use '/workspaces' as directory
    # default is the google colab directory
    parser.add_argument('--DIR', '--dir', '-d', type=str, help='Directory path to dataset folder', default)
    parser.add_argument('--classId', '--id', '-ci', type=int, help='ID of the class to be displayed, if none is given all classes will be displayed')
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