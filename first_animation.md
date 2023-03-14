~~~ json
{
    "init_images": [pil_to_base64(current_frame)],#Plug converted Image to Payload
    "prompt": "best quality, perfect lighting, shiny skin, manga , looking at the viewer, forest ruins, golden black magical medival armor, exposed belly,white hair, golden eyes,long hair,pointy ears",
    "negative_prompt": "(longbody),(extra fingers), (missing fingers), (extra limb), (bad anatomy), (bad proportions),(worst quality, low quality, blurry:1.4), big breast",
    "steps": 20,
    "denoising_strength": 0.4,
    "seed": 3562534656,
    "sampler_name": "Euler a",
    "cfg_scale": 4,
    "width": 1024,
    "height": 1024,
    "sampler_index": "Euler a",
}

{
    "init_images": [pil_to_base64(current_frame)],#Plug converted Image to Payload
    "prompt": "best quality, perfect lighting, shiny skin, manga , looking at the viewer, forest ruins, golden black magical medival armor, exposed belly,white hair, golden eyes,long hair,pointy ears",
    "negative_prompt": "(longbody),(extra fingers), (missing fingers), (extra limb), (bad anatomy), (bad proportions),(worst quality, low quality, blurry:1.4), big breast",
    "steps": 20,
    "denoising_strength": 0.75,
    "seed": 3562534656,
    "sampler_name": "Euler a",
    "cfg_scale": 4,
    "width": 1024,
    "height": 1024,
    "controlnet_input_image":[pil_to_base64(video_frame)],
    "controlnet_module": 'openpose',
    "controlnet_model": 'control_sd15_openpose [fef5e48e]',
    "controlnet_resize_mode": "Scale to Fit (Inner Fit)",
    "controlnet_weight": 2,
    "controlnet_guidance": 1,
    "sampler_index": "Euler a",
}
~~~