import torch
import numpy as np
import random
import copy
import functools
import tqdm

# own files
import utils
from pulsar_methods import Pulsar

print("### importing warnings ###")

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

print("### defining methods ###")

def run_experiment(iters=1):
    accs = []
    for i in range(iters):
        print("#"*75)
        # m_sz = (model.config.sample_size, model.config.sample_size)
        img_sz = pipe.unet.config.sample_size
        m_sz = (img_sz**2 // 512) * 200
        # m_sz = 25600
        # m_sz = 1600
        m = np.random.randint(2, size=m_sz)
        k = tuple(int(r) for r in np.random.randint(1000, size=(3,)))
        # k = (10, 11, 12)
        print(f"Iteration {i+1} using keys {k}")
        # prompt = "Portrait photo of a man with mustache."
        prompt = """
        A close-up shot Photo of a young woman lying on the grass. 
        She has long brown hair that cascades around her head, blending with the green blades of grass. 
        Her eyes are closed, giving her a serene and peaceful expression. 
        She has a light complexion with a few freckles on her cheeks. 
        Her lips are slightly parted, and she wears a subtle, natural shade of lipstick that 
        complements her soft, delicate features. 
        The woman is dressed in a black dress with small floral patterns, 
        adding a touch of elegance to the natural setting. 
        The dress features a mix of white and brown flowers, 
        which blend harmoniously with the green and earthy tones of the surroundings. 
        The background consists of lush, green grass that provides a soft bed for the woman. 
        The grass is slightly overgrown, with a few wildflowers scattered throughout, 
        adding a touch of color and wild beauty to the scene. 
        There are some tall grass stalks and weeds gently swaying in the breeze, 
        indicating a natural, untouched meadow. 
        The setting is outdoors, and the overall atmosphere is calm and tranquil, 
        suggesting a warm, sunny day in the countryside. 
        The lighting is natural and soft, with the sun casting a gentle, warm glow over the scene. 
        The light filters through the grass, creating a dappled effect on the woman's face and dress. 
        This soft lighting enhances the serene mood of the photograph, 
        making it appear as though the woman is in a state of deep relaxation or possibly asleep. 
        The shadows are minimal and soft, contributing to the overall dreamy quality of the image. 
        It's a cinematic scene with cinematic and soft natural lighting, 
        emphasizing the peacefulness and beauty of the moment. 
        The composition is well-balanced, with the woman's face as the focal point, 
        drawing the viewer's eye to her serene expression and the delicate details of her features. 
        The close-up shot allows for an intimate perspective, 
        making the viewer feel as if they are right there in the meadow with her, 
        sharing in the tranquility of the moment. 
        The overall scene evokes a sense of harmony with nature. 
        The combination of the woman's peaceful demeanor, the natural setting, 
        and the soft, natural lighting creates a feeling of calm and serenity. 
        This image captures a perfect moment of relaxation and connection with the natural world, 
        making it both visually appealing and emotionally evocative.
        """
        p = Pulsar(pipe, k, timesteps, prompt=prompt)
        print("ENCODING")
        img = p.encode(m)
        print("DECODING")
        out = p.decode(img)
        print(f"length of m is {len(m)}")
        print(f"length of out is {len(out)}")
        acc = utils.calc_acc(m, out)
        accs.append(acc)
        print(f"Run accuracy {acc}")
    print("#"*75)
    print(f"Final Average Accuracy {np.mean(accs)}")

print("### importing pipeline ###")

device = "cuda" if torch.cuda.is_available() else "cpu"
use_stable = True

if use_stable:
    from diffusers import StableDiffusionImg2ImgPipeline
    from diffusers import StableDiffusionPipeline

    model_id_or_path = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
    pipe = pipe.to(device)
else:
    from diffusers import DDIMPipeline

    repos = [
        "google/ddpm-church-256",
        "google/ddpm-bedroom-256",
        "google/ddpm-cat-256",
        "google/ddpm-celebahq-256"
    ]
    model_id_or_path = repos[0]
    pipe = DDIMPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
    pipe = pipe.to(device)

# timesteps = 3
timesteps = 50


print("### running experiments ###")

# img = pipe(
#     "A photo of a cat"
# ).images[0]

# img.save("sd3_hello_world-no-T5.png")

run_experiment(10)