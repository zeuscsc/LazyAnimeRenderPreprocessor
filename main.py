import argparse
import subprocess
import os
from PIL import Image
import glob
from mask import mask
from crop import crop
from tqdm import tqdm
from parallel_tasks_queuer import build_and_execute

REFRENCE_IMAGE=None

def mask_pbar_wrapper(*args):
    mask(*args)
    mask_pbar.update(1)
def crop_pbar_wrapper(*args):
    crop(*args)
    crop_pbar.update(1)
def crop_iterator_generator(file,output_path,square=False):
    crop_iterator=[]
    refrence_height=refrence_width=768
    if square is False:
        refrence_width,refrence_height = REFRENCE_IMAGE.size
    if refrence_height > refrence_width:
        crop_iterator.append((file,output_path,512,768))
    if refrence_height < refrence_width:
        crop_iterator.append((file,output_path,768,512))
    if refrence_height == refrence_width or square:
        crop_iterator.append((file,output_path,768,768))
    return crop_iterator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path","-f", type=str, default=None,help="video path")
    parser.add_argument("--background_image_path","-b", type=str, default=None,help="video path")
    args = parser.parse_args()
    video_path=args.video_path
    background_image_path=args.background_image_path
    base_name, extension = os.path.splitext(video_path)
    raw_folder = base_name+"/raw"
    inputs_folder = base_name+"/inputs"
    masked_folder = base_name+"/masked"
    cropped_folder = base_name+"/cropped"
    train_ds_folder = base_name+"/train_ds"
    if not os.path.exists(raw_folder):
        os.makedirs(raw_folder)
        cmd = f'ffmpeg -i "{video_path}" "{raw_folder}/%04d.png"'
        subprocess.call(cmd, shell=True)
    files = glob.glob(os.path.join(raw_folder, '*.png'))
    if not os.path.exists(masked_folder):
        os.makedirs(masked_folder)
    if not os.path.exists(cropped_folder):
        os.makedirs(cropped_folder)
    if not os.path.exists(inputs_folder):
        os.makedirs(inputs_folder)
    if not os.path.exists(train_ds_folder):
        os.makedirs(train_ds_folder)
    print("Preparing threads queue...")
    crop_iterator=[]
    mask_iterator=[]
    for file in tqdm(files):
        filename = os.path.basename(file)
        if REFRENCE_IMAGE is None:
            REFRENCE_IMAGE = Image.open(file)
        cropped_path = f'{cropped_folder}/{filename}'
        crop_iterator+=crop_iterator_generator(file,cropped_path)
        crop_iterator+=crop_iterator_generator(file,train_ds_folder,True)
        masked_path = f'{masked_folder}/{filename}'
        background_image=None
        if background_image_path is not None:
            
            inputs_path = f'{inputs_folder}/{filename}'
            mask_iterator.append((file,inputs_path,background_image_path))
            crop_iterator+=crop_iterator_generator(inputs_path,inputs_path)
        mask_iterator.append((file,masked_path,None))
        crop_iterator+=crop_iterator_generator(masked_path,masked_path)
    print("Masking images...")
    with tqdm(total=len(mask_iterator)) as mask_pbar:
        # mask_iterator=[mask_iterator[0]]
        build_and_execute(mask_iterator,mask_pbar_wrapper,16,True,0)
        # exit()
    print("Cropping images...")
    with tqdm(total=len(crop_iterator)) as crop_pbar:
        build_and_execute(crop_iterator,crop_pbar_wrapper,16,True,0)
