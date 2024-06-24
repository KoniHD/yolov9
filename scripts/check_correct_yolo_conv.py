import os
import argparse
import json

missing_img_annotation = []
missing_img_json = []
printMissing = True

def check_sum(img_dir, label_dir):
    num_img_files = len(os.listdir(os.path.join(img_dir, 'train'))) \
        + len(os.listdir(os.path.join(img_dir, 'val')))
    num_label_files = len(os.listdir(os.path.join(label_dir, 'train'))) \
        + len(os.listdir(os.path.join(label_dir, 'val')))

    if num_img_files != num_label_files:
        print(f"Number of images and labels do not match: image files {num_img_files} \
               and label files {num_label_files}")
        print(f"Checking for images without annotations.")
        check_missing_annotation(img_dir, label_dir)

def check_missing_annotation(img_dir, label_dir):
    for img_file in os.listdir(os.path.join(img_dir, 'train')):
        if img_file.replace("jpg", "txt") not in os.listdir(os.path.join(label_dir, 'train')):
            missing_img_annotation.append(img_file)
    for img_file in os.listdir(os.path.join(img_dir, 'val')):
        if img_file.replace("jpg", "txt") not in os.listdir(os.path.join(label_dir, 'val')):
            missing_img_annotation.append(img_file)
    
    if len(missing_img_annotation) > 0 and printMissing:
        print(f"Images without annotations:")
        for img in missing_img_annotation:
            print(img)
    print(f"Total number of images without annotations: {len(missing_img_annotation)}")

def checkJSON(json_dir):
    with open(json_dir, 'r') as f:
        json_data = json.load(f)
        for img in missing_img_annotation:
            if img not in json_data["images"]:
                missing_img_json.append(img)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir', '--img', '-i', type=str, help='Directory path to image folder', default='/content/yolov9/loco/images')
    parser.add_argument('--label_dir', '--label', '-l', type=str, help='Directory path to label folder', default='/content/yolov9/loco/labels')
    parser.add_argument('--checkJSON', '--json', '-j', type=str, help='Check provided JSON files for missing annotations')
    parser.add_argument('--quite', '-q', action='store_true', help='Do not print out missing annotations')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arg = parse_args()
    printMissing = not arg.quite
    check_sum(arg.img_dir, arg.label_dir)
    if arg.checkJSON:
        checkJSON(arg.checkJSON)
        if len(missing_img_json) > 0:
            print(f"Number of images also without annotations in JSON: {len(missing_img_json)}")
