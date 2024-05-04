import shutil, os
import argparse

# This script is used to transform the dataset to the YOLO format
# For use in GitHub Codespaces use '/workspaces' instead of content
def transformToYoloFormat(HOME='/content/yolov9/loco/images'):
    # to use the dataset should be in the yolov9 directory
    original_dir = os.path.join(HOME)
    temp_dir = os.path.join(HOME, '../', 'temp')

    # supported image extensions
    image_extensions = {".jpg", ".jpeg"}
    custom_structure = False

    # check if the dataset is already in the YOLO format and keep the structure
    if os.path.exists(os.path.join(original_dir, 'train')):
        transformToYoloFormat(os.path.join(original_dir, 'train'))
        os.rename(os.path.join(original_dir, 'temp'), os.path.join(original_dir, 'train'))
        custom_structure = True
    if os.path.exists(os.path.join(original_dir, 'val')):
        transformToYoloFormat(os.path.join(original_dir, 'val'))
        os.rename(os.path.join(original_dir, 'temp'), os.path.join(original_dir, 'val'))
        custom_structure = True
    if os.path.exists(os.path.join(original_dir, 'test')):
        transformToYoloFormat(os.path.join(original_dir, 'test'))
        os.rename(os.path.join(original_dir, 'temp'), os.path.join(original_dir, 'test'))
        custom_structure = True
    if custom_structure:
        return

    # copy all images to a temp directory
    os.makedirs(temp_dir, exist_ok=True)
    for dir_name, sub_dir_list, file_list in os.walk(original_dir):
        for file_name in file_list:
            if any(file_name.lower().endswith(ext) for ext in image_extensions):
                source = os.path.join(dir_name, file_name)
                destination = os.path.join(temp_dir, file_name)
                shutil.move(source, destination)

    shutil.rmtree(original_dir)

def parse_args():
    parser = argparse.ArgumentParser()
    # for use in GitHub Codespaces use '/workspaces' as directory
    # default is the google colab directory
    parser.add_argument('--DIR', '--dir', type=str, help='Directory path', default='/content/yolov9/loco/images')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arg = parse_args()
    transformToYoloFormat(arg.DIR)