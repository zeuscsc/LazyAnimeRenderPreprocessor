import cv2
import mediapipe as mp
import numpy as np
import os
import glob

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

BG_COLOR = (0, 0, 0) # black
MASK_COLOR = (255, 255, 255) # white

with mp_selfie_segmentation.SelfieSegmentation(
    model_selection=0) as selfie_segmentation:
    path = 'video_frames_source/frames'
    files = glob.glob(os.path.join(path, '*.jpg'))
    scene_image = cv2.imread('video_frames_source/scene.png')
    last_fg_image = None
    for file in files:
        filename = os.path.basename(file)
        image = cv2.imread(file)
        image_height, image_width, _ = image.shape
        results = selfie_segmentation.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        blurred_image = cv2.GaussianBlur(image,(255,255),0)
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        fg_image = np.zeros(image.shape, dtype=np.uint8)
        fg_image[:] = MASK_COLOR
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        if not os.path.exists('video_frames_source/masks'):
            os.mkdir('video_frames_source/masks')
        if not os.path.exists('video_frames_source/inputs'):
            os.mkdir('video_frames_source/inputs')
        if last_fg_image is not None:
            merged_mask = cv2.bitwise_or(fg_image, last_fg_image)
            output_image = np.where(condition, merged_mask, bg_image)
            cv2.imwrite(f'video_frames_source/masks/{filename}', output_image)
            cv2.imwrite(f'video_frames_source/inputs/{filename}', scene_image)
        last_fg_image=fg_image
