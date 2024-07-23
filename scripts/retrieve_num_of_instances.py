"""
This script is intended to get picture ids containing a given category id from the LOCO dataset.
Potential Ids are:
  0: small_load_carrier
  1: forklift
  2: pallet
  3: stillage
  4: pallet_truck
Parameters
----------
dir : str
    Directory path to label folder. It might contain the subdirectories `train`, `val` and `test` 
class-id: int
    Id of the class to be searched. Possible Ids are 0 (small load carrier), 1 (forklift), \
        2 (pallet), 3 (stillage), 4 (pallet truck)
"""

import os
import argparse

def get_filenames_of_id(dir, subdir, classId):
    numOfInstances = 0
    file_list = []
    # create file to store the list of files containing the classId
    with open (f"InstancesIn_{subdir}.txt", 'w') as listOfFiles:
        for file in os.listdir(os.path.join(dir, subdir)):
            contains_id = False

            # open file and check if classId is in the file
            with open(os.path.join(dir, subdir, file), 'r') as f:
                if classId is None:
                    numOfInstances += sum(1 for line in f)
                    filename, _ = os.path.splitext(file)
                    file_list.append(filename + '.jpg')
                else:
                    for line in f:
                        data = line.strip().split()
                        if int(data[0]) in classId:
                            numOfInstances += 1
                            if not contains_id:
                                filename, _ = os.path.splitext(file)
                                file_list.append(filename + '.jpg')
                                listOfFiles.write(f"{filename}.jpg\n")
                                contains_id = True
    if classId is None:
        os.remove(f"InstancesIn_{subdir}.txt")

    return len(file_list), numOfInstances


def num_instances(dir, classId):
    numInstances = 0
    for file in os.listdir(dir):
        with open(os.path.join(dir, file), 'r') as f:
            for line in f:
                data = line.strip().split()
                if int(data[0]) in classId:
                    numInstances += 1
    return numInstances

def to_set(arg):
    return set(map(lambda x: int(x.strip()), arg.split(',')))

def parse_args():
    parser = argparse.ArgumentParser()
    # for use in GitHub Codespaces use '/workspaces' as directory
    # default is the google colab directory
    parser.add_argument('--dir', '-d', type=str, help='Directory path to label folder', default='/content/yolov9/loco')
    parser.add_argument('--class-id', '--id', type=to_set, help='Comma-seperated list of Class IDs to be searched. \
                        If none is given all classes will be displayed.')
    parser.add_argument('--num-instances', action='store_true', help='If set, the num instances will be searched instead of num images')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arg = parse_args()

    if not os.path.exists(arg.dir):
        raise FileNotFoundError(f"Directory {arg.dir} does not exist")
    if arg.class_id and not all(isinstance(i, int) and 0<=i and i<=4 for i in arg.class_id):
        raise ValueError(f"Class ID {arg.class_id} is not valid. Valid IDs are 0, 1, 2, 3, 4.")
    
    numOfInstances = 0
    
    if arg.num_instances:
        numOfInstances = num_instances(os.path.abspath(arg.dir), arg.class_id)
        print(f"Total number of instances of category {arg.class_id} is {numOfInstances}.")
        exit(0)
    
    if os.path.exists(os.path.join(arg.dir, 'train')):
        numOfImages, numOfInstancesTrain = get_filenames_of_id(os.path.abspath(arg.dir), 'train', arg.class_id)
        numOfInstances += numOfInstancesTrain
        if arg.class_id is not None:
            print(f"There are {numOfImages} images containing an object of category {arg.class_id} in the train dataset." +
                  " The image_files are located in the file InstancesIn_train.txt.")
        else:
            print(f"There are {numOfImages} images in the train dataset containing an annotated object.")
    if os.path.exists(os.path.join(arg.dir, 'val')):
        numOfImages, numOfInstancesVal = get_filenames_of_id(os.path.abspath(arg.dir), 'val', arg.class_id)
        numOfInstances += numOfInstancesVal
        if arg.class_id is not None:
            print(f"There are {numOfImages} images containing an object of category {arg.class_id} in the val dataset." +
                  " The image_files are located in the file InstancesIn_val.txt.")
        else:
            print(f"There are {numOfImages} images in the val dataset containing an annotated object.")
    if os.path.exists(os.path.join(arg.dir, 'test')):
        numOfImages, numOfInstancesTest = get_filenames_of_id(os.path.abspath(arg.dir), 'test', arg.class_id)
        numOfInstances += numOfInstancesTest
        if arg.class_id is not None:
            print(f"There are {numOfImages} images containing an object of category {arg.class_id} in the test dataset." +
                  " The image_files are located in the file InstancesIn_test.txt.")
        else:
            print(f"There are {numOfImages} images in the test dataset containing an annotated object.")
    print(f"Total number of images of category {arg.class_id} is {numOfInstances}")