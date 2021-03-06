# Copyright 2020 Lorna Authors. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import argparse
import glob
import os

import torch.utils.data
import torchvision.transforms as transforms
from PIL import Image
from tqdm import tqdm

from esrgan_pytorch import check_image_file
from esrgan_pytorch import utils

parser = argparse.ArgumentParser(description="Low resolution image generation using bicubic simple down sampling.")
parser.add_argument("--input-dir", type=str, required=True, help="Folder for low resolution images.")
parser.add_argument("--target-dir", type=str, required=True, help="Folder for high resolution images.")
parser.add_argument("--cleanup-factor", default=2, type=int, help="downscaling factor for image cleanup. (default: 2).")
parser.add_argument("--upscale-factor", default=4, type=int, help="upscale factor for image. (default: 4).")
args = parser.parse_args()

lr_dir = f"./{args.upscale_factor}x/input"
hr_dir = f"./{args.upscale_factor}x/target"
lr_files = [os.path.join(args.input_dir, x) for x in os.listdir(args.input_dir) if check_image_file(x)]
hr_files = [os.path.join(args.target_dir, x) for x in os.listdir(args.target_dir) if check_image_file(x)]

# Make sure the folder is empty.
assert not os.path.exists(lr_dir)
assert not os.path.exists(hr_dir)

try:
    os.makedirs(lr_dir)
    os.makedirs(hr_dir)
except OSError:
    pass

pil2tensor = transforms.ToTensor()
tensor2pil = transforms.ToPILImage()

# Get all kernelGAN distribute file
kernel_paths = glob.glob(os.path.join(args.kernel_dir, f"*/*_kernel_{args.upscale_factor}x.mat"))


def process_for_lr():
    r""" The low resolution data set is preliminarily processed.
    """
    for filename in tqdm(lr_files, desc="Generating images from lr dir"):
        img = Image.open(filename)
        img = pil2tensor(img)

        # Remove noise
        img = utils.imresize(img, 1.0 / args.cleanup_factor, True)
        _, w, h = img.size()
        w = w - w % args.upscale_factor
        h = h - h % args.upscale_factor
        img = img[:, :w, :h]

        # Save high resolution img
        img = tensor2pil(img)
        img.save(os.path.join(args.hr_dir, os.path.basename(filename)), "bmp")

        # Simple down sampling.
        img = utils.imresize(img, 1.0 / args.upscale_factor, True)

        # Save low resolution img
        img = tensor2pil(img)
        img.save(os.path.join(args.lr_dir, os.path.basename(filename)), "bmp")


def process_for_hr():
    r""" The high resolution data set is preliminarily processed.
    """
    for filename in tqdm(hr_files, desc="Generating images from hr dir"):
        img = Image.open(filename)
        img = pil2tensor(img)

        # Save high resolution img
        img = tensor2pil(img)
        img.save(os.path.join(args.hr_dir, os.path.basename(filename)), "bmp")

        # Simple down sampling.
        img = utils.imresize(img, 1.0 / args.upscale_factor, True)

        # Save low resolution img
        img = tensor2pil(img)
        img.save(os.path.join(args.lr_dir, os.path.basename(filename)), "bmp")


if __name__ == "__main__":
    with torch.no_grad():
        process_for_lr()
        process_for_hr()
