import cv2
import mediapipe as mp
import numpy as np
import os
import argparse
from PIL import Image

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

BG_COLOR = (0, 0, 0) # black
MASK_COLOR = (255, 255, 255) # white

def mask(path:str,output_path:str,background_image:np.ndarray=None):
    with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=0) as selfie_segmentation:
        image = Image.open(path)
        image = np.array(image)
        image_height, image_width, _ = image.shape
        results = selfie_segmentation.process(image)
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        fg_image = np.zeros(image.shape, dtype=np.uint8)
        fg_image[:] = MASK_COLOR
        if background_image is None:
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            output_image = np.where(condition, fg_image, bg_image)
        else:
            np.array(background_image)
            bg_image = cv2.resize(background_image, (image_width, image_height))
            output_image = np.where(condition, image, bg_image)
        # cv2.imwrite(f'{output_path}', output_image)
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
