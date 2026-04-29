import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join('..'))
from scripts.augment import insert_image

DATA_DIR = os.path.join('.data')
PCB_DIR = os.path.join(DATA_DIR, 'base')
OUT_DIR = os.path.join(DATA_DIR, 'base-prepared')


def find_least_rotated_image(images: list[np.ndarray]) -> tuple[np.ndarray, int]:
    least_rotated_img = 0
    least_black_pixels = float('inf')
    for i, img in enumerate(images):
        num_black_pixels = np.sum(img == 0)
        if num_black_pixels < least_black_pixels:
            least_black_pixels = num_black_pixels
            least_rotated_img = i
    return images[least_rotated_img], least_rotated_img

for split in ['train', 'valid', 'test']:
    split_dir = os.path.join(PCB_DIR, split)
    split_images = os.listdir(os.path.join(split_dir, 'images'))
    pcbs = {t.split('.rf')[0]: [i for i in split_images if i.startswith(t.split('.rf')[0])] for t in split_images}
    for pcb in pcbs.items():
        pcb_id, images = pcb
        imgs = [plt.imread(os.path.join(split_dir, 'images', img)) for img in images]

        # Find the least rotated image and save it
        least_rotated_img, ix = find_least_rotated_image(imgs)
        output_path = os.path.join(OUT_DIR, f"{pcb_id}.png")
        plt.imsave(output_path, least_rotated_img)


processed_files = os.listdir(OUT_DIR)
print(f"Number of processed pcbs: {len(processed_files)}")