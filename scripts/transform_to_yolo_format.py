"""
This script converts annotation data from LOCO format (COCO based) to YOLO format. It has two options:
1. Extracting the images from subdirectories inside the `image` directory and moving them all in the root of `image`.
    If a custom data split inside `images` of train, val and test is present the script will maintain this structure.
2. Converting the annotations in JSON format (COCO style) to YOLO format.
    Additionally it creates a `loco.yaml` file in the root of the dataset folder with the class names.

Parameters
----------
dir : str
    Directory path to dataset folder. It should contain the subdirectories `images` and `labels` with the images and annotations in COCO format.
    This option must be provided in order for the script to work.
convert-images : store_true
    If set, the script will extract images from subdirectories inside the `images` directory and move them all in the root of `images`.
    If a custom data split inside `images` of train, val and test is present the script will maintain this structure.
convert-annotations : store_true
    If set, the script will convert dataset annotations from COCO to YOLO format.
"""

import shutil, os
import argparse
import json
from tqdm import tqdm

def convert_bbox_coco2yolo(img_width, img_height, bbox):
    """
    Convert bounding box from COCO  format to YOLO format

    Parameters
    ----------
    img_width : int
        width of image
    img_height : int
        height of image
    bbox : list[int]
        bounding box annotation in COCO format:
        [top left x position, top left y position, width, height]

    Returns
    -------
    list[float]
        bounding box annotation in YOLO format:
        [x_center_rel, y_center_rel, width_rel, height_rel]
    """

    # YOLO bounding box format: [x_center, y_center, width, height]
    # (float values relative to width and height of image)
    x_tl, y_tl, w, h = bbox

    dw = 1.0 / img_width
    dh = 1.0 / img_height

    x_center = x_tl + w / 2.0
    y_center = y_tl + h / 2.0

    x = x_center * dw
    y = y_center * dh
    w = w * dw
    h = h * dh

    return [x, y, w, h]

def convert_classid_coco2yolo(loco_id):
    """
    Convert class ID from COCO to YOLO format

    Parameters
    ----------
    loco_id : int
        class ID in LOCO format

    Returns
    -------
    int
        class ID in YOLO format
    """
    # LOCO class IDs are not sorted, YOLO class IDs are 0-indexed
    if loco_id == 3:
        return 0
    elif loco_id == 5:
        return 1
    elif loco_id == 7:
        return 2
    elif loco_id == 10:
        return 3
    elif loco_id == 11:
        return 4
    else:
        raise ValueError(f"Unknown class ID {loco_id}")

# This script is used to transform the dataset to the YOLO format
# For use in GitHub Codespaces use '/workspaces' instead of content
def transform_images_to_yolo_format(directory):
    temp_dir = os.path.abspath(os.path.join(directory, '../', 'temp'))

    # supported image extensions
    image_extensions = {".jpg", ".jpeg"}
    custom_structure = False

    # check if the dataset is already in the YOLO format and keep the structure
    if os.path.exists(os.path.join(directory, 'train')):
        transform_images_to_yolo_format(os.path.join(directory, 'train'))
        os.rename(os.path.join(directory, 'temp'), os.path.join(directory, 'train'))
        custom_structure = True
    if os.path.exists(os.path.join(directory, 'val')):
        transform_images_to_yolo_format(os.path.join(directory, 'val'))
        os.rename(os.path.join(directory, 'temp'), os.path.join(directory, 'val'))
        custom_structure = True
    if os.path.exists(os.path.join(directory, 'test')):
        transform_images_to_yolo_format(os.path.join(directory, 'test'))
        os.rename(os.path.join(directory, 'temp'), os.path.join(directory, 'test'))
        custom_structure = True
    if custom_structure:
        print("Finished working on images with custom structure")
        return

    # copy all images to a temp directory
    os.makedirs(temp_dir, exist_ok=True)
    for dir_name, sub_dir_list, file_list in tqdm(os.walk(directory), desc=f"Sorting images in {directory}"):
        for file_name in file_list:
            if any(file_name.lower().endswith(ext) for ext in image_extensions):
                source = os.path.join(dir_name, file_name)
                destination = os.path.join(temp_dir, file_name)
                shutil.move(source, destination)

    shutil.rmtree(directory)

def convert_json_to_yolo_txt(directory):

    custom_structure = False
    if os.path.exists(os.path.join(directory, 'train')):
        convert_json_to_yolo_txt(os.path.join(directory, 'train'))
        custom_structure = True
    if os.path.exists(os.path.join(directory, 'val')):
        convert_json_to_yolo_txt(os.path.join(directory, 'val'))
        custom_structure = True
    if os.path.exists(os.path.join(directory, 'test')):
        convert_json_to_yolo_txt(os.path.join(directory, 'test'))
        custom_structure = True
    if custom_structure:
        print("Finished working on labels with custom structure")
        return

    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

    for json_file in tqdm(json_files, desc=f"Converting JSON to YOLO in {directory}"):
        with open(os.path.join(directory, json_file)) as f:
            json_data = json.load(f)
        for image in json_data["images"]:
            img_id = image["id"]
            img_name = image["file_name"]
            img_width = image["width"]
            img_height = image["height"]

            anno_in_image = [anno for anno in json_data["annotations"] if anno["image_id"] == img_id]
            anno_txt = os.path.join(directory, img_name.replace(".jpg", ".txt"))
            with open(anno_txt, "w") as f:
                for anno in anno_in_image:
                    class_id = convert_classid_coco2yolo(anno["category_id"])
                    bbox_COCO = anno["bbox"]
                    x, y, w, h = convert_bbox_coco2yolo(img_width, img_height, bbox_COCO)
                    f.write(f"{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
        os.remove(os.path.join(directory, json_file))

def create_loco_yaml(directory):
    class_names = []
    classes_found = False
    for dir_name, sub_dir_list, file_list in os.walk(directory):
        if classes_found:
            break
        for file in file_list:
            if file.endswith('.json'):
                with open(os.path.join(dir_name, file)) as f:
                    json_data = json.load(f)
                for category in json_data["categories"]:
                    class_names.append(category["name"])
                classes_found = True
                break
    
    if os.path.exists(os.path.join(directory, 'loco.yaml')):
        return
    
    with open(os.path.abspath(os.path.join(directory, '../../' 'loco.yaml')), 'w') as f:
        if os.path.exists(os.path.join(directory, 'train')):
            f.write(f"train: {os.path.abspath(os.path.join(directory, '../images/', 'train'))}\n")
        else:
            f.write(f"path: {directory}\n")
        if os.path.exists(os.path.join(directory, 'val')):
            f.write(f"val: {os.path.abspath(os.path.join(directory, '../images/', 'val'))}\n")
        if os.path.exists(os.path.join(directory, 'test')):
            f.write(f"test: {os.path.abspath(os.path.join(directory, '../images/', 'test'))}\n")
        f.write('\nnc: 5\nnames:')
        for i, name in enumerate(class_names):
            f.write(f'\n  {i}: {name}')
        

def parse_args():
    parser = argparse.ArgumentParser()
    # for use in GitHub Codespaces use '/workspaces' as directory
    # default is the google colab directory
    parser.add_argument('--dir', '-d', type=str, help='Directory path to dataset folder', default='/content/yolov9/loco')
    parser.add_argument('--convert-annotations', action='store_true', help='Convert dataset annotation from COCO (JSON) to YOLO format')
    parser.add_argument('--convert-images', action='store_true', help='Extract images from subdirectories and move them to the root of the images directory')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arg = parse_args()
    if not os.path.exists(arg.dir):
        raise FileNotFoundError(f"Directory {arg.dir} does not exist")
    if arg.convert_images:
        if os.path.exists(os.path.join(arg.dir, 'images')):
            transform_images_to_yolo_format(os.path.join(arg.dir, 'images'))
        else:
            raise FileNotFoundError(f"Subdirectory 'images' not found in {arg.dir}")
    if arg.convert_annotations:
        if os.path.exists(os.path.join(arg.dir, 'labels')):
            create_loco_yaml(os.path.join(arg.dir, 'labels'))
            convert_json_to_yolo_txt(os.path.join(arg.dir, 'labels'))
        else:
            raise FileNotFoundError(f"Subdirectory 'labels' not found in {arg.dir}")