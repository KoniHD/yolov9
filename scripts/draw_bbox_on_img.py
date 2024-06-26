"""
This script takes a given bbox represented in the yolo format in a .txt file and draws it on the corresponding image.

Parameters
----------
dir : str
    Path to dataset directory. It should contain the subdirectories `images` and `labels` 
class-id: int
    Comma-seperated list of Class IDs to be displayed, if none is given all classes will be displayed.
    Possible Ids are 0 (small load carrier), 1 (forklift), 2 (pallet), 3 (stillage), 4 (pallet truck)
img: str
    Name of the image to be displayed. E.g. '1574676405.192456.jpg' for a forklift picture.
    Images are stored in the subdirectory `bbox_anot` after the script is executed.
shifted-bbox: bool
    If Ture produces another additional file ('img_shifted.jpg') with shifted bounding boxes.
    Default is False.
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

def get_predictions(dir, subset, imgName, classId):

    predictions = []
    labels = os.path.splitext(imgName)[0] + ".txt"
    image = cv.imread(os.path.join(dir, 'images/', subset, imgName))
    img_height, img_width = image.shape[:2]

    with open(os.path.join(dir, 'labels/', subset, labels), 'r') as f:
        for line in f:
            data = line.strip().split()
            if classId is None or int(data[0]) in classId:
                predictions.append({
                    'x': float(data[1]) * img_width,
                    'y': float(data[2]) * img_height,
                    'width': float(data[3]) * img_width,
                    'height': float(data[4]) * img_height,
                    'classId': int(data[0]),
                })
    
    return predictions, image

def draw_bbs(dir, subset, imgName, classId):

    predictions, image = get_predictions(dir, subset, imgName, classId)
    
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
            class_names[bounding_box['classId']],
            (int(x0), int(y1) + 20),
            fontFace = cv.FONT_HERSHEY_TRIPLEX,
            fontScale = 0.7,
            color = (255, 255, 255),
            thickness=1
        )
    if not os.path.exists(os.path.join(dir, 'bbox_anot/')):
        os.mkdir(os.path.abspath(os.path.join(dir, 'bbox_anot/')))
    cv.imwrite(os.path.join(dir, 'bbox_anot/', imgName), image)

def draw_shifted_bbx(dir, subset, imgName, classId):

    predictions, image = get_predictions(dir, subset, imgName, classId)
    imgName = os.path.splitext(imgName)[0] + "_shifted.jpg"
    img_height, img_width = image.shape[:2]

    for bounding_box in predictions:
        x0 = bounding_box['x'] - bounding_box['width'] / 2 + 0.04 * img_width
        x1 = bounding_box['x'] + bounding_box['width'] / 2 + 0.04 * img_width
        y0 = bounding_box['y'] - bounding_box['height'] / 2 + 0.04 * img_height
        y1 = bounding_box['y'] + bounding_box['height'] / 2 + 0.04 * img_height
    
        start_point = (int(x0), int(y0))
        end_point = (int(x1), int(y1))
        cv.rectangle(image, start_point, end_point, color=(0,0,255), thickness=2)
    
        cv.putText(
            image,
            "misplaced BB",
            (int(x0), int(y1) + 20),
            fontFace = cv.FONT_HERSHEY_TRIPLEX,
            fontScale = 0.7,
            color = (255, 255, 255),
            thickness=1
        )
    if not os.path.exists(os.path.join(dir, 'bbox_anot/')):
        os.mkdir(os.path.abspath(os.path.join(dir, 'bbox_anot/')))
    cv.imwrite(os.path.join(dir, 'bbox_anot/', imgName), image)

def to_set(arg):
    return set(map(lambda x: int(x.strip()), arg.split(',')))

def parse_args():
    parser = argparse.ArgumentParser()
    # for use in GitHub Codespaces use '/workspaces' as directory
    # for use of LRZ AI systems use '/workspace' as directory
    # default is the google colab directory
    parser.add_argument('--dir', '-d', type=str, help='Path to dataset directory.', default='/content/yolov9/loco')
    parser.add_argument('--class-id', '--id', type=to_set, help='Comma-seperated list of Class IDs to be displayed. \
                        If none is given all classes will be displayed.')
    parser.add_argument('--img', type=str, help='Filename of the image to be displayed.')
    parser.add_argument('--shifted-bbox', '--sbb', action='store_true', help='Produces another file with shifted bounding boxes.\
                        Default is Flase')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arg = parse_args()
    
    if not os.path.exists(arg.dir):
        raise FileNotFoundError(f"Directory {arg.dir} does not exist")
    if arg.classId and not all(isinstance(i, int) and 0<=i and i<=4 for i in arg.classId):
        raise ValueError(f"Class ID {arg.classId} is not valid. Valid IDs are {class_names.keys()}")

    if os.path.exists(os.path.join(arg.dir, 'images/train', arg.img)):
        draw_bbs(os.path.abspath(arg.dir), 'train', arg.img, arg.classId)
        if arg.shiftedBbox:
            draw_shifted_bbx(os.path.abspath(arg.dir), 'train', arg.img, arg.classId)
    elif os.path.exists(os.path.join(arg.dir, 'images/val', arg.img)):
        draw_bbs(os.path.abspath(arg.dir), 'val', arg.img, arg.classId)
        if arg.shiftedBbox:
            draw_shifted_bbx(os.path.abspath(arg.dir), 'val', arg.img, arg.classId)
    elif os.path.exists(os.path.join(arg.dir, 'images/test', arg.img)):
        draw_bbs(os.path.abspath(arg.dir), 'val', arg.img, arg.classId)
        if arg.shiftedBbox:
            draw_shifted_bbx(os.path.abspath(arg.dir), 'val', arg.img, arg.classId)
    else:
        raise FileNotFoundError(f"Image {arg.img} does not exist")