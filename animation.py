import os
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from io import BytesIO

url = "http://localhost:7860"

PROMPT="[file bolum],(red clothes),(magenta coat),(black loliter),church"
NEGATIVE_PROMPT="[file neg]"
SAMPLER_NAME="DPM++ SDE Karras"
SKIP_SAMPLES_COUNT=1
OFFSET=1
SIZE=512

init_image = Image.open("video_frames_source/init.png")
init_image = init_image.resize((SIZE,SIZE))

def pil_to_base64(pil_image):
    with BytesIO() as stream:
        pil_image.save(stream, "PNG", pnginfo=None)
        base64_str = str(base64.b64encode(stream.getvalue()), "utf-8")
        return "data:image/png;base64," + base64_str

def render_frame(current_frame,masked_frame,control_frame):
    global frame_index
    payload = {
        "init_images": [pil_to_base64(current_frame)],#Plug converted Image to Payload
        "prompt": PROMPT,
        "negative_prompt": NEGATIVE_PROMPT,
        "steps": 20,
        "denoising_strength": 0.525,
        "seed": 884396570,
        "sampler_name": SAMPLER_NAME,
        "sampler_index": SAMPLER_NAME,
        "cfg_scale": 7,
        "width": SIZE,
        "height": SIZE,
        "controlnet_input_image":[pil_to_base64(control_frame)],
        "controlnet_mask": [pil_to_base64(masked_frame)],
        "controlnet_module": 'openpose',
        "controlnet_model": 'control_sd15_openpose [fef5e48e]',
        "controlnet_resize_mode": "Scale to Fit (Inner Fit)",
        "controlnet_weight": 2,
        "controlnet_guidance": 1,
    }
    response = requests.post(url=f'{url}/controlnet/img2img', json=payload)
    r = response.json()
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        return image,pnginfo

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

save_dir_path=f"video_frames_source/output"
if not os.path.exists(save_dir_path):
    os.mkdir(save_dir_path)
    pass
frame_index=1
load_dir_path = "video_frames_source/frames"
mask_dir_path = "video_frames_source/masks"
file_names = os.listdir(load_dir_path)
current_frame = init_image
for file_name in file_names:
    if frame_index%SKIP_SAMPLES_COUNT==0 and frame_index>OFFSET:
        control_frame = Image.open(os.path.join(load_dir_path, file_name))
        mask_frame = Image.open(os.path.join(mask_dir_path, file_name))
        mask_frame = resize_image(mask_frame)
        control_frame = resize_image(control_frame)
        current_frame,pnginfo = render_frame(current_frame,mask_frame,control_frame)
        current_frame.save(f'{save_dir_path}/{frame_index}.png', pnginfo=pnginfo)
        print(f"Saved {frame_index}.png")
    frame_index+=1
    pass