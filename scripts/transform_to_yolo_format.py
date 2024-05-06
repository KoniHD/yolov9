import shutil, os
import argparse
import json
import shutil
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

# This script is used to transform the dataset to the YOLO format
# For use in GitHub Codespaces use '/workspaces' instead of content
def transform_images_to_yolo_format(directory='/content/yolov9/loco/images'):
    temp_dir = os.path.join(directory, '../', 'temp')

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

    # write labels, which holds names of all classes (one class per line)
    # label_file = os.path.join(os.path.join(output_path, "../"), "labels.txt")
    # with open(label_file, "w") as f:
    #    for category in tqdm(json_data["categories"], desc="Categories"):
    #        category_name = category["name"]
    #        f.write(f"{category_name}\n")

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
            anno_txt = os.path.join(directory, img_name.split(".")[0] + ".txt")
            with open(anno_txt, "w") as f:
                for anno in anno_in_image:
                    class_id = anno["category_id"]
                    bbox_COCO = anno["bbox"]
                    x, y, w, h = convert_bbox_coco2yolo(img_width, img_height, bbox_COCO)
                    f.write(f"{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
        os.remove(os.path.join(directory, json_file))

def parse_args():
    parser = argparse.ArgumentParser()
    # for use in GitHub Codespaces use '/workspaces' as directory
    # default is the google colab directory
    parser.add_argument('--DIR', '--dir', type=str, help='Directory path to dataset folder', default='/content/yolov9/loco')
    parser.add_argument('--convert2yolo', '-c2y', '--coco2yolo', action='store_true', help='Convert dataset from COCO to YOLO format')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arg = parse_args()
    if not os.path.exists(arg.DIR):
        raise FileNotFoundError(f"Directory {arg.DIR} does not exist")
    transform_images_to_yolo_format(os.path.join(arg.DIR, 'images'))
    if arg.convert2yolo:
        if os.path.exists(os.path.join(arg.DIR, 'labels')):
            convert_json_to_yolo_txt(os.path.join(arg.DIR, 'labels'))
        else:
            convert_json_to_yolo_txt(arg.DIR)