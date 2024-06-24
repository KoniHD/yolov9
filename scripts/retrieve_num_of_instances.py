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
DIR : str
    Directory path to label folder. It might contain the subdirectories `train`, `val` and `test` 
classID: int
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

def to_set(arg):
    return set(map(lambda x: int(x.strip()), arg.split(',')))

def parse_args():
    parser = argparse.ArgumentParser()
    # for use in GitHub Codespaces use '/workspaces' as directory
    # default is the google colab directory
    parser.add_argument('--dir', '-d', type=str, help='Directory path to label folder', default='/content/yolov9/loco')
    parser.add_argument('--classId', '--id', type=to_set, help='Comma-seperated list of Class IDs to be searched. \
                        If none is given all classes will be displayed.')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arg = parse_args()

    if not os.path.exists(arg.dir):
        raise FileNotFoundError(f"Directory {arg.dir} does not exist")
    if arg.classId and not all(isinstance(i, int) and 0<=i and i<=4 for i in arg.classId):
        raise ValueError(f"Class ID {arg.classId} is not valid. Valid IDs are 0, 1, 2, 3, 4.")
    
    numOfInstances = 0
    
    if os.path.exists(os.path.join(arg.dir, 'train')):
        numOfImages, numOfInstancesTrain = get_filenames_of_id(os.path.abspath(arg.dir), 'train', arg.classId)
        numOfInstances += numOfInstancesTrain
        if arg.classId is not None:
            print(f"There are {numOfImages} images containing an object of category {arg.classId} in the train dataset." +
                  " The image_files are located in the file InstancesIn_train.txt.")
        else:
            print(f"There are {numOfImages} images in the train dataset containing an annotated object.")
    if os.path.exists(os.path.join(arg.dir, 'val')):
        numOfImages, numOfInstancesVal = get_filenames_of_id(os.path.abspath(arg.dir), 'val', arg.classId)
        numOfInstances += numOfInstancesVal
        if arg.classId is not None:
            print(f"There are {numOfImages} images containing an object of category {arg.classId} in the val dataset." +
                  " The image_files are located in the file InstancesIn_val.txt.")
        else:
            print(f"There are {numOfImages} images in the val dataset containing an annotated object.")
    if os.path.exists(os.path.join(arg.dir, 'test')):
        numOfImages, numOfInstancesTest = get_filenames_of_id(os.path.abspath(arg.dir), 'test', arg.classId)
        numOfInstances += numOfInstancesTest
        if arg.classId is not None:
            print(f"There are {numOfImages} images containing an object of category {arg.classId} in the test dataset." +
                  " The image_files are located in the file InstancesIn_test.txt.")
        else:
            print(f"There are {numOfImages} images in the test dataset containing an annotated object.")
    print(f"Total number of images of category {arg.classId} is {numOfInstances}")