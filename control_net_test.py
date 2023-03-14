import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from io import BytesIO
import json

url = "http://localhost:7860"


img = Image.open("test_samples/00000.png")
img = img.resize((512,512))
img_mask=Image.new("RGB",(img.width,img.height),(255,255,255))

video_frame=Image.open("test_samples/video_frames/0001.jpg")
video_mask=Image.new("RGB",(video_frame.width,video_frame.height),(255,255,255))
# video_frame = video_frame.resize((512,512))

def pil_to_base64(pil_image):
    with BytesIO() as stream:
        pil_image.save(stream, "PNG", pnginfo=None)
        base64_str = str(base64.b64encode(stream.getvalue()), "utf-8")
        return "data:image/png;base64," + base64_str
    
payload = {
    "init_images": [pil_to_base64(img)],#Plug converted Image to Payload
    "prompt": "best quality, perfect lighting, shiny skin, manga , looking at the viewer, forest ruins, golden black magical medival armor, exposed belly,white hair, golden eyes,long hair,pointy ears",
    "negative_prompt": "(longbody),(extra fingers), (missing fingers), (extra limb), (bad anatomy), (bad proportions),(worst quality, low quality, blurry:1.4), big breast",
    "steps": 20,
    "denoising_strength": 0.75,
    "seed": 2454023504,
    "sampler_name": "Euler a",
    "cfg_scale": 7,
    "width": 512,
    "height": 512,
    "batch_size":4,
    "controlnet_input_image":[pil_to_base64(video_frame)],
    "controlnet_module": 'openpose',
    "controlnet_model": 'control_sd15_openpose [fef5e48e]',
    "controlnet_resize_mode": "Scale to Fit (Inner Fit)",
    "controlnet_weight": 1,
    "controlnet_guidance": 1,
    "sampler_name": "string",
    "sampler_index": "Euler a",
}    
# response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
response = requests.post(url=f'{url}/controlnet/img2img', json=payload)
r = response.json()

# with open("output.json", "w") as outfile:
#     json.dump(r, outfile)

image_index=1
for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    image.save(f'test_samples/output{image_index}.png', pnginfo=pnginfo)
    image_index+=1