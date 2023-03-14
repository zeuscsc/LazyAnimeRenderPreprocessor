import os
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from io import BytesIO

url = "http://localhost:7860"

PROMPT="((masterpiece, best quality)), ( single girl) , (looking at the viewer), (forest ruins:1.2), (golden black magical medival armor:1.5), (slim and fit exposed belly:1.5),(white hair), (golden eyes),(long hair),(pointy ears),"
NEGATIVE_PROMPT="(worst quality, low quality:1.4), EasyNegative , bad_prompt_version2, (big breast),(no pony tail),fat"
SAMPLER_NAME="DPM++ SDE Karras"
SKIP_SAMPLES_COUNT=1

init_image = Image.open("video_frames_source/init.png")
init_image = init_image.resize((1024,1024))

def pil_to_base64(pil_image):
    with BytesIO() as stream:
        pil_image.save(stream, "PNG", pnginfo=None)
        base64_str = str(base64.b64encode(stream.getvalue()), "utf-8")
        return "data:image/png;base64," + base64_str

def render_frame(current_frame,video_frame,is_init_image=False):
    global frame_index
    if is_init_image:
        payload = {
            "init_images": [pil_to_base64(current_frame)],#Plug converted Image to Payload
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE_PROMPT,
            "steps": 20,
            "denoising_strength": 0.05,
            "seed": 2914170809,
            "sampler_name": SAMPLER_NAME,
            "sampler_index": SAMPLER_NAME,
            "cfg_scale": 7,
            "width": 1024,
            "height": 1024,
            "script_name":"img2img alternative test",
            "script_args":[None,True,True,PROMPT,NEGATIVE_PROMPT,True,10,True,1,0,True]
        }
        response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    else:
        payload = {
            "init_images": [pil_to_base64(current_frame)],#Plug converted Image to Payload
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE_PROMPT,
            "steps": 20,
            "denoising_strength": 0.25,
            "seed": 2977116445,
            "sampler_name": SAMPLER_NAME,
            "sampler_index": SAMPLER_NAME,
            "cfg_scale": 7,
            "width": 1024,
            "height": 1024,
            "controlnet_input_image":[pil_to_base64(video_frame)],
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

save_dir_path=f"video_frames_source/output"
if not os.path.exists(save_dir_path):
    os.mkdir(save_dir_path)
    pass
frame_index=0
load_dir_path = "video_frames_source/frames"
file_names = os.listdir(load_dir_path)
current_frame = init_image
for file_name in file_names:
    if frame_index%SKIP_SAMPLES_COUNT==0:
        video_frame = Image.open(os.path.join(load_dir_path, file_name))
        current_frame,pnginfo = render_frame(current_frame,video_frame,True)
        current_frame,pnginfo = render_frame(current_frame,video_frame)
        current_frame.save(f'{save_dir_path}/{frame_index}.png', pnginfo=pnginfo)
        print(f"Saved {frame_index}.png")
    frame_index+=1
    pass