import os
from PIL import Image

SIZE=512
def resize_image(image):
    width, height = image.size
    size = min(width, height)
    left = (width - size) / 2
    top = (height - size) / 2
    right = (width + size) / 2
    bottom = (height + size) / 2
    img_cropped = image.crop((left, top, right, bottom))
    img_resized = img_cropped.resize((SIZE, SIZE))
    img_resized.save('resized_image.jpg')
    return img_resized

root_dir="C:/Users/user/Pictures/Ai_Arts/work/tecky_media/Poster/training_samples/cusonlo"
load_dir_path = f"{root_dir}/raw"
file_names = os.listdir(load_dir_path)
for file_name in file_names:
    try:
        img = Image.open(os.path.join(load_dir_path, file_name))
        img = resize_image(img)
        if not os.path.exists(f'{root_dir}/resized'):
            os.mkdir(f'{root_dir}/resized')
        img.save(f'{root_dir}/resized/{file_name}')
    except:
        print(f'error: {file_name}')