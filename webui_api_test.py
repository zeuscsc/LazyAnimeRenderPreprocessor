import webuiapi
from PIL import Image

api = webuiapi.WebUIApi(host="localhost", port=7860, use_https=False, 
                        sampler="Euler a", steps=20)

# create API client with custom host, port
#api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)

# create API client with custom host, port and https
#api = webuiapi.WebUIApi(host='webui.example.com', port=443, use_https=True)

# create API client with default sampler, steps.
#api = webuiapi.WebUIApi(sampler='Euler a', steps=20)

img = Image.open("test_samples/00000.png")
img = img.resize((512,512))
result2 = api.img2img(images=[img], 
                    prompt="best quality, perfect lighting, shiny skin, manga , looking at the viewer, forest ruins, golden black magical medival armor, exposed belly,white hair, golden eyes,long hair,pointy ears",
                    negative_prompt="(longbody),(extra fingers), (missing fingers), (extra limb), (bad anatomy), (bad proportions),(worst quality, low quality, blurry:1.4), big breast",
                    seed=2454023504, 
                    cfg_scale=7, 
                    denoising_strength=0.75,
                    steps=20
                    # batch_size=4
                    )
result2.image.save("test_samples/output.png", "PNG")
# result2.image[0].save("test_samples/output1.png", "PNG")
# result2.image[1].save("test_samples/output2.png", "PNG")
# result2.image[2].save("test_samples/output3.png", "PNG")
# result2.image[3].save("test_samples/output4.png", "PNG")
