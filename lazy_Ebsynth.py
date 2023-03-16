import argparse
import os
import glob
from tqdm import tqdm
from PIL import Image
import shutil

REFRENCE_IMAGE=None

def get_path(folder_name):
    path=os.path.join(ROOT_DIR_PATH,folder_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mixing_image_path","-f", type=str, default=None,help="mixing image path")
    args = parser.parse_args()
    mixing_image_path=args.mixing_image_path
    base_name, extension = os.path.splitext(mixing_image_path)
    ROOT_DIR_PATH=os.path.dirname(mixing_image_path)
    video_key_path=os.path.join(ROOT_DIR_PATH,"video_key")
    files = glob.glob(os.path.join(video_key_path, '*.png'))
    inputs_folder = get_path("inputs")
    masked_folder = get_path("masked")
    control_folder = get_path("control")
    for file in tqdm(files):
        filename = os.path.basename(file)
        input_path = os.path.join(inputs_folder,filename)
        shutil.copy(mixing_image_path, input_path)
        masked_path = os.path.join(masked_folder,filename)
        shutil.copy(os.path.join(get_path("video_mask"),filename), masked_path)
        control_path = os.path.join(control_folder,filename)
        shutil.copy(os.path.join(get_path("video_frame"),filename), control_path)
        
        
        