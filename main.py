import argparse
from math import floor
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
def crop_iterator_generator(file,output_path,square=False,train_ds=False):
    crop_iterator=[]
    refrence_height=refrence_width=768
    if square is False:
        refrence_width,refrence_height = REFRENCE_IMAGE.size
    if train_ds is True:
        refrence_height=refrence_width=512
    if refrence_height > refrence_width:
        crop_iterator.append((file,output_path,512,768))
    if refrence_height < refrence_width:
        crop_iterator.append((file,output_path,768,512))
    if refrence_height == refrence_width and train_ds is False:
        crop_iterator.append((file,output_path,768,768))
    if train_ds is True:
        crop_iterator.append((file,output_path,512,512))
    return crop_iterator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path","-f", type=str, default=None,help="video path")
    parser.add_argument("--background_image_path","-b", type=str, default=None,help="video path")
    parser.add_argument("--mask_background","-m", action="store_true")
    parser.add_argument("--convert2binary","-B", action="store_true")
    args = parser.parse_args()
    video_path=args.video_path
    mask_background=args.mask_background
    background_image_path=args.background_image_path
    convert2binary=args.convert2binary
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
    sampling=floor(len(files)/40)
    index=0
    crop_iterator=[]
    mask_iterator=[]
    for file in tqdm(files):
        filename = os.path.basename(file)
        if REFRENCE_IMAGE is None:
            REFRENCE_IMAGE = Image.open(file)
        cropped_path = f'{cropped_folder}/{filename}'
        crop_iterator+=crop_iterator_generator(file,cropped_path)
        train_ds_path = f'{train_ds_folder}/{filename}'
        if index%sampling==0:
            crop_iterator+=crop_iterator_generator(file,train_ds_path,train_ds=True)
        masked_path = f'{masked_folder}/{filename}'
        background_image=None
        if background_image_path is not None:
            inputs_path = f'{inputs_folder}/{filename}'
            if mask_background:
                mask_iterator.append((file,inputs_path,background_image_path,True,convert2binary))
            else:
                mask_iterator.append((file,inputs_path,background_image_path,False,convert2binary))
            crop_iterator+=crop_iterator_generator(inputs_path,inputs_path)
        mask_iterator.append((file,masked_path,None,False,convert2binary))
        crop_iterator+=crop_iterator_generator(masked_path,masked_path)
        index+=1
    print("Masking images...")
    with tqdm(total=len(mask_iterator)) as mask_pbar:
        # mask_pbar_wrapper(*mask_iterator[0])
        # exit()
        build_and_execute(mask_iterator,mask_pbar_wrapper,16,True,0)
    print("Cropping images...")
    with tqdm(total=len(crop_iterator)) as crop_pbar:
        build_and_execute(crop_iterator,crop_pbar_wrapper,16,True,0)
