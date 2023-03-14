import os
from PIL import Image
import argparse

def resize_image(image,wanted_width=512,wanted_height=768):
    new_size = (wanted_width, wanted_height)
    width, height = image.size
    if width > height:
        new_width = int(height * (new_size[0] / new_size[1]))
        new_height = height
    else:
        new_width = width
        new_height = int(width * (new_size[1] / new_size[0]))
    
    # Crop the image from the center
    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = left + new_width
    bottom = top + new_height
    cropped_image = image.crop((left, top, right, bottom))
    
    # Resize the image to the new size
    resized_image = cropped_image.resize(new_size, Image.ANTIALIAS)
    return resized_image
def crop(path:str,output_path:str, width:int, height:int):
    img = Image.open(path)
    img = resize_image(img,width,height)
    img.save(f'{output_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path","-f", type=str, default=None,
                        help="image path")
    parser.add_argument("--width","-W", type=int, default=None,
                        help="image width")
    parser.add_argument("--height","-H", type=int, default=None,
                        help="image height")
    args = parser.parse_args()
    path=args.image_path
    if args.width is not None:
        WIDTH=args.width
    if args.height is not None:
        HEIGHT=args.height
    if path is None:
        print("Please provide image path")
        exit(1)
    filename = os.path.basename(path)
    base_name, extension = os.path.splitext(filename)
    new_filename = base_name+"_cropped" + ".png"
    crop(path,new_filename,WIDTH,HEIGHT)