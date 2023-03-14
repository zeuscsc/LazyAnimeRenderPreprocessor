import argparse
import subprocess
import os
import cv2
import glob
from mask import mask
from crop import crop

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path","-v", type=str, default=None,help="video path")
    args = parser.parse_args()
    video_path=args.video_path
    base_name, extension = os.path.splitext(video_path)
    raw_folder = base_name+"_frames/raw"
    masked_folder = base_name+"_frames/masked"
    cropped_folder = base_name+"_frames/cropped"
    if not os.path.exists(raw_folder):
        os.makedirs(raw_folder)
        cmd = f'ffmpeg -i "{video_path}" "{raw_folder}/%04d.png"'
        subprocess.call(cmd, shell=True)
    files = glob.glob(os.path.join(raw_folder, '*.png'))
    if not os.path.exists(masked_folder):
        os.makedirs(masked_folder)
    if not os.path.exists(cropped_folder):
        os.makedirs(cropped_folder)
    for file in files:
        filename = os.path.basename(file)
        image = cv2.imread(file)
        image_height, image_width, _ = image.shape
        cropped_path = f'{cropped_folder}/{filename}'
        if image_height > image_width:
            crop(file,cropped_path,512,768)
        if image_height < image_width:
            crop(file,cropped_path,768,512)
        if image_height == image_width:
            crop(file,cropped_path,768,768)
        masked_path = f'{masked_folder}/{filename}'
        mask(cropped_path,masked_path)
