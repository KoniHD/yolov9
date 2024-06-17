import os
import argparse

class_transform = {
    1: '0',
    2: '1',
    3: '2',
    4: '3',
    5: '4'
}

def remove_person_class(dir):
    for file in os.listdir(dir):
        with open(os.path.join(dir, file), 'r') as f:
            lines = f.readlines()
        with open(os.path.join(dir, file), 'w') as f:
            for line in lines:
                data = line.strip().split()
                if int(data[0]) == 0:
                    continue
                f.write(' '.join([class_transform[int(data[0])]] + data[1:]))
                f.write('\n')
                
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', '-d', type=str, help='Directory path to label folder', default='data/labels')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    arg = parse_args()
    remove_person_class(arg.dir)