import torch
import numpy as np
import random
import copy
import functools
import tqdm

# own files
from utils import *
from pulsar_methods import encode, decode

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
        m_sz = 25600
        m = np.random.randint(2, size=m_sz)
        # k = tuple(int(r) for r in np.random.randint(1000, size=(3,)))
        k = (10, 11, 12)
        print(f"Iteration {i+1} using keys {k}")
        print("ENCODING")
        img = encode(pipe, timesteps, m, k, device)
        print("DECODING")
        out = decode(pipe, timesteps, img, k, device)
        acc = calc_acc(m, out)
        accs.append(acc)
        print(f"Run accuracy {acc}")
    print("#"*75)
    print(f"Final Average Accuracy {np.mean(accs)}")

print("### importing model+scheduler ###")

device = "cuda" if torch.cuda.is_available() else "cpu"
use_stable = False

if use_stable:
    from diffusers import StableDiffusionImg2ImgPipeline

    model_id_or_path = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
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

run_experiment(1)