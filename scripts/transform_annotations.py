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
convert-to-yolo : store_true
    If set, the script will convert dataset annotations from COCO to YOLO format.
convert-to-coco : store_true
    If set, the script will aggregate annotations into single train/val/test files in COCO format.
custom-train-val : str
    Three lists seperated by / to set custom train/val/test split based on LOCO subsets.
    Default: "2,3,5/1,4/"
"""

import shutil, os, re
import argparse
import json
from tqdm import tqdm

class_indices = {
    3: 0,   # small_load_carrier
    5: 1,   # forklift
    7: 2,   # pallet
    10: 3,  # stillage
    11: 4   # pallet_truck
}

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

# This script is used to transform the dataset to the YOLO format
# For use in GitHub Codespaces use '/workspaces' instead of content
def transform_images_to_yolo_format(dir):
    temp_dir = os.path.abspath(os.path.join(dir, '../', 'temp'))

    # supported image extensions
    image_extensions = {".jpg", ".jpeg"}
    custom_structure = False

    # check if the dataset is already in the YOLO format and keep the structure
    if os.path.exists(os.path.join(dir, 'train')):
        transform_images_to_yolo_format(os.path.join(dir, 'train'))
        os.rename(os.path.join(dir, 'temp'), os.path.join(dir, 'train'))
        custom_structure = True
    if os.path.exists(os.path.join(dir, 'val')):
        transform_images_to_yolo_format(os.path.join(dir, 'val'))
        os.rename(os.path.join(dir, 'temp'), os.path.join(dir, 'val'))
        custom_structure = True
    if os.path.exists(os.path.join(dir, 'test')):
        transform_images_to_yolo_format(os.path.join(dir, 'test'))
        os.rename(os.path.join(dir, 'temp'), os.path.join(dir, 'test'))
        custom_structure = True
    if custom_structure:
        print("Finished working on images with custom structure")
        return

    # copy all images to a temp directory
    os.makedirs(temp_dir, exist_ok=True)
    for dir_name, _, file_list in tqdm(os.walk(dir), desc=f"Sorting images in {dir}"):
        for file_name in file_list:
            if any(file_name.lower().endswith(ext) for ext in image_extensions):
                source = os.path.join(dir_name, file_name)
                destination = os.path.join(temp_dir, file_name)
                shutil.move(source, destination)

    shutil.rmtree(dir)

# Needs refactoring:
# - Find out if .6f is not too much precision
# - Images w/o annotations should get empty .txt files
def convert_json_to_yolo_txt(dir):

    custom_structure = False
    if os.path.exists(os.path.join(dir, 'train')):
        convert_json_to_yolo_txt(os.path.join(dir, 'train'))
        custom_structure = True
    if os.path.exists(os.path.join(dir, 'val')):
        convert_json_to_yolo_txt(os.path.join(dir, 'val'))
        custom_structure = True
    if os.path.exists(os.path.join(dir, 'test')):
        convert_json_to_yolo_txt(os.path.join(dir, 'test'))
        custom_structure = True
    if custom_structure:
        print("Finished working on labels with custom structure")
        return

    json_files = [f for f in os.listdir(dir) if f.endswith('.json')]

    for json_file in tqdm(json_files, desc=f"Converting JSON to YOLO in {dir}"):
        with open(os.path.join(dir, json_file), 'r') as f:
            json_data = json.load(f)
        for image in json_data["images"]:
            img_id = image["id"]
            img_name = image["file_name"]
            img_width = image["width"]
            img_height = image["height"]

            anno_in_image = [anno for anno in json_data["annotations"] if anno["image_id"] == img_id]
            anno_txt = os.path.join(dir, img_name.replace(".jpg", ".txt"))
            with open(anno_txt, "w") as f:
                for anno in anno_in_image:
                    class_id = class_indices[anno["category_id"]]
                    bbox_COCO = anno["bbox"]
                    x, y, w, h = convert_bbox_coco2yolo(img_width, img_height, bbox_COCO)
                    f.write(f"{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
        os.remove(os.path.join(dir, json_file))

def create_loco_yaml(dir):
    class_names = []
    classes_found = False
    for dir_name, _, file_list in os.walk(dir):
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
    
    if os.path.exists(os.path.join(dir, 'loco.yaml')):
        return
    
    with open(os.path.abspath(os.path.join(dir, '../../' 'loco.yaml')), 'w') as f:
        if os.path.exists(os.path.join(dir, 'train')):
            f.write(f"train: {os.path.abspath(os.path.join(dir, '../images/', 'train'))}\n")
        else:
            f.write(f"path: {dir}\n")
        if os.path.exists(os.path.join(dir, 'val')):
            f.write(f"val: {os.path.abspath(os.path.join(dir, '../images/', 'val'))}\n")
        if os.path.exists(os.path.join(dir, 'test')):
            f.write(f"test: {os.path.abspath(os.path.join(dir, '../images/', 'test'))}\n")
        f.write('\nnc: 5\nnames:')
        for i, name in enumerate(class_names):
            f.write(f'\n  {i}: {name}')

def aggregate_coco_annotations(dir, name=None):
    aggregated_data = {"images": [], "categories": [], "annotations": []}

    custom_structure = False
    if os.path.exists(os.path.join(dir, 'train')):
        aggregate_coco_annotations(os.path.join(dir, 'train'), 'train')
        custom_structure = True
    if os.path.exists(os.path.join(dir, 'val')):
        aggregate_coco_annotations(os.path.join(dir, 'val'), 'val')
        custom_structure = True
    if os.path.exists(os.path.join(dir, 'test')):
        aggregate_coco_annotations(os.path.join(dir, 'test'), 'test')
        custom_structure = True
    if custom_structure:
        print("Finished working on labels with custom structure")
        return
    
    json_files = [f for f in os.listdir(dir) if f.endswith('.json')]
    for json_file in json_files:
        with open(os.path.join(dir, json_file), 'r') as f:
            json_data = json.load(f)
            for anno in json_data["annotations"]:
                anno["category_id"] = class_indices[anno["category_id"]]
            aggregated_data["images"].extend(json_data["images"])
            aggregated_data["categories"].extend(json_data["categories"])
            aggregated_data["annotations"].extend(json_data["annotations"])
        os.remove(os.path.join(dir, json_file))
    
    if aggregated_data["images"] and aggregated_data["categories"] and aggregated_data["annotations"]:
        with open(os.path.join(dir, f'{name}-subset.json'), 'w') as f:
            json.dump(aggregated_data, f)
        print(f"Aggregated annotations for {name} subset finished")



def set_train_val_split(dir, train, val, test):
    labels_dir = os.path.abspath(os.path.join(dir, 'labels'))
    images_dir = os.path.abspath(os.path.join(dir, 'images'))

    os.makedirs(os.path.join(labels_dir, 'train'), exist_ok=True)
    os.makedirs(os.path.join(labels_dir, 'val'), exist_ok=True)
    os.makedirs(os.path.join(labels_dir, 'test'), exist_ok=True)
    os.makedirs(os.path.join(images_dir, 'train'), exist_ok=True)
    os.makedirs(os.path.join(images_dir, 'val'), exist_ok=True)
    os.makedirs(os.path.join(images_dir, 'test'), exist_ok=True)

    for _, subdir, file_list in os.walk(os.path.join(labels_dir)):
        subdir.clear()
        for file_name in file_list:
            if file_name.endswith('.json'):
                match = re.search(r'sub(\d+)', file_name)
                if match and int(match.group(1)) in train:
                    shutil.move(os.path.join(labels_dir, file_name), os.path.join(labels_dir, 'train', file_name))
                elif match and int(match.group(1)) in val:
                    shutil.move(os.path.join(labels_dir, file_name), os.path.join(labels_dir, 'val', file_name))
                elif match and (int(match.group(1)) in test):
                    shutil.move(os.path.join(labels_dir, file_name), os.path.join(labels_dir, 'test', file_name))

    for _, subdir, _ in os.walk(os.path.join(images_dir)):
        for subset in subdir:
            match = re.search(r'(\d+)', subset)
            if match and int(match.group(1)) in train:
                shutil.move(os.path.join(images_dir, subset), os.path.join(images_dir, 'train', subset))
            elif match and int(match.group(1)) in val:
                shutil.move(os.path.join(images_dir, subset), os.path.join(images_dir, 'val', subset))
            elif match and int(match.group(1)) in test:
                shutil.move(os.path.join(images_dir, subset), os.path.join(images_dir, 'test', subset))
        subdir.clear()



def three_lists(arg):
    try:
        # Split the input string by '/' to separate the two lists
        split_subset = arg.split('/')
        if len(split_subset) != 3:
            raise argparse.ArgumentTypeError("Input must be two lists of integers separated by a slash")
        
        # For each part, split by ',' and convert each item to an integer
        if split_subset[0]:
            train_subset = [int(item) for item in split_subset[0].split(',')]
        else:
            train_subset = []
        if split_subset[1]:
            val_subset = [int(item) for item in split_subset[1].split(',')]
        else:
            val_subset = []
        if split_subset[2]:
            test_subset = [int(item) for item in split_subset[2].split(',')]
        else:
            test_subset = []
        
        return train_subset, val_subset, test_subset
    except ValueError:
        # Raise an error if conversion to integer fails
        raise argparse.ArgumentTypeError("Each list must contain integers separated by commas")

def parse_args():
    parser = argparse.ArgumentParser()
    # for use in GitHub Codespaces use '/workspaces' as directory
    # default is the google colab directory
    parser.add_argument('--dir', '-d', type=str, help='Directory path to dataset folder', default='/content/loco')
    parser.add_argument('--convert-to-yolo', action='store_true', help='Convert dataset annotation from COCO (JSON) to YOLO format.')
    parser.add_argument('--convert-images', action='store_true', help='Extract images from subdirectories and move them to the root of the images directory.')
    parser.add_argument('--convert-to-coco', action='store_true', help='Aggregates annotations into train/val files in COCO format.')
    parser.add_argument('--custom-train-val', type=three_lists, default="2,3,5/1,4/", help='Three lists seperated by / to set custom train/val/test split based on LOCO subsets.')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arg = parse_args()
    if not os.path.exists(arg.dir):
        raise FileNotFoundError(f"Directory {arg.dir} does not exist")
    if arg.convert_to_yolo and arg.convert_to_coco:
        raise ValueError("Only one conversion option can be selected")
    
    if not all(1 <= num <= 5 for num in arg.custom_train_val[0]) and \
        all(1 <= num <= 5 for num in arg.custom_train_val[1]) and \
        all(1 <= num <= 5 for num in arg.custom_train_val[2]):
        raise ValueError("Custom train/val split is not supported yet")
    set_train_val_split(arg.dir, arg.custom_train_val[0], arg.custom_train_val[1], arg.custom_train_val[2])

    if arg.convert_images:
        if os.path.exists(os.path.join(arg.dir, 'images')):
            transform_images_to_yolo_format(os.path.join(arg.dir, 'images'))
        else:
            raise FileNotFoundError(f"Subdirectory 'images' not found in {arg.dir}")
    if arg.convert_to_yolo:
        if os.path.exists(os.path.join(arg.dir, 'labels')):
            create_loco_yaml(os.path.join(arg.dir, 'labels'))
            convert_json_to_yolo_txt(os.path.join(arg.dir, 'labels'))
        else:
            raise FileNotFoundError(f"Subdirectory 'labels' not found in {arg.dir}")
    if arg.convert_to_coco:
        aggregate_coco_annotations(os.path.join(arg.dir, 'labels'))