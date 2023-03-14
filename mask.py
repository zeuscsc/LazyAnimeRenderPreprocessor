import cv2
import mediapipe as mp
import numpy as np
import os
import argparse
from PIL import Image,ImageDraw

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

BG_COLOR = (0, 0, 0) # black
MASK_COLOR = (255, 255, 255) # white

last_frame = None

def mask(path:str,output_path:str,background_image_path:str=None):
    global last_frame
    with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=0) as selfie_segmentation:
        image = Image.open(path)
        # ImageDraw.floodfill(image, (1,1), (0,255,0), thresh=50)
        ImageDraw.floodfill(image, (1476, 966), (0,255,0), thresh=25)
        ImageDraw.floodfill(image, (1510, 897), (0,255,0), thresh=25)
        ImageDraw.floodfill(image, (1781, 910), (0,255,0), thresh=25)
        image = np.array(image)
        image_height, image_width, _ = image.shape
        results = selfie_segmentation.process(image)
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        fg_image = np.zeros(image.shape, dtype=np.uint8)
        fg_image[:] = MASK_COLOR
        if background_image_path is None:
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            output_image = np.where(condition, fg_image, bg_image)
            if last_frame is not None:
                output_image=cv2.bitwise_or(output_image,last_frame)
                
            last_frame=np.where(condition, fg_image, bg_image)
        else:
            background_image=Image.open(background_image_path)
            background_image=background_image.convert("RGB")
            background_image=np.array(background_image)
            bg_image = cv2.resize(background_image, (image_width, image_height))
            output_image = np.where(condition, image, bg_image)


        Image.fromarray(output_image).save(f'{output_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path","-f", type=str, default=None,
                        help="image path")
    args = parser.parse_args()
    path=args.image_path
    if path is None:
        print("Please provide image path")
        exit(1)

    filename = os.path.basename(path)
    base_name, extension = os.path.splitext(filename)
    new_filename = base_name+"_masked" + ".png"
    mask(path,new_filename)
