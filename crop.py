import os
from PIL import Image
import argparse

def resize_image(image,width=512,height=768):
    # Resize the image to fit within the maximum width and height while maintaining the aspect ratio
    _width, _height = image.size
    aspect_ratio = _width / _height
    if _width > width:
        _width = width
        _height = int(_width / aspect_ratio)
    if _height > height:
        _height = height
        _width = int(_height * aspect_ratio)
    image = image.resize((_width, _height))
    return image
def crop(path:str,output_folder_path:str, width:int, height:int):
    img = Image.open(path)
    img = resize_image(img,width,height)
    filename = os.path.basename(path)
    base_name, extension = os.path.splitext(filename)
    new_filename = base_name+"_cropped" + ".png"
    img.save(f'{output_folder_path}/{new_filename}')

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
    folder_path = os.path.dirname(path)
    crop(path,folder_path,WIDTH,HEIGHT)