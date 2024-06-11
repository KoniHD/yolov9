"""
This script is intended to get picture ids containing a given id from the LOCO dataset.
Potential Ids are:
  0: small_load_carrier
  1: forklift
  2: pallet
  3: stillage
  4: pallet_truck
Parameters
----------
DIR : str
    Directory path to label folder. It might contain the subdirectories `train`, `val` and `test` 
fileID: int
    Id of the class to be searched
"""

import os
import argparse

def get_filenames_of_id(id, dir, subdir):
    file_list = []
    with open (f"InstancesIn_{subdir}.txt", 'w') as listOfFiles:
        for file in os.listdir(os.path.join(dir, subdir)):
            with open(os.path.join(dir, subdir, file), 'r') as f:
                for line in f:
                    class_id = int(line.split()[0])
                    if class_id == id:
                        filename, _ = os.path.splitext(file)
                        file_list.append(filename + '.jpg')
                        listOfFiles.write(f"{filename}.jpg\n")
                        break
    return len(file_list), listOfFiles


def parse_args():
    parser = argparse.ArgumentParser()
    # for use in GitHub Codespaces use '/workspaces' as directory
    # default is the google colab directory
    parser.add_argument('--DIR', '--dir', '-d', type=str, help='Directory path to label folder', default='/workspace/yolov9/loco')
    parser.add_argument('--fileId', '--id', '-fi', type=int, help='ID of the class to be searched')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arg = parse_args()
    if not os.path.exists(arg.DIR):
        raise FileNotFoundError(f"Directory {arg.DIR} does not exist")
    if os.path.exists(os.path.join(arg.DIR, 'train')):
        numOfInstances, listOfFiles = get_filenames_of_id(arg.fileId, os.path.abspath(arg.DIR), 'train')
        print(f"There are {numOfInstances} images of category {arg.fileId} in the train dataset. Located in the file InstancesIn_train.txt.")
    if os.path.exists(os.path.join(arg.DIR, 'val')):
        numOfInstances, listOfFiles = get_filenames_of_id(arg.fileId, os.path.abspath(arg.DIR), 'val')
        print(f"There are {numOfInstances} images of category {arg.fileId} in the val dataset. Located in the file InstancesIn_val.txt.")
    if os.path.exists(os.path.join(arg.DIR, 'test')):
        numOfInstances, listOfFiles = get_filenames_of_id(arg.fileId, os.path.abspath(arg.DIR), 'test')
        print(f"There are {numOfInstances} images of category {arg.fileId} in the test dataset. Located in the file InstancesIn_test.txt.")