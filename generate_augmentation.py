import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join('..'))
from scripts.augment import insert_image

DATA_DIR = os.path.join('.data')

BACKGROUND_DIR = os.path.join(DATA_DIR, 'background')
DISTRACTIONS_DIR = os.path.join(DATA_DIR, 'distraction')
PCB_DIR = os.path.join(DATA_DIR, 'base-prepared')

background_images = [os.path.join(BACKGROUND_DIR, f) for f in os.listdir(BACKGROUND_DIR) if f.endswith('.png')]
distraction_images = [os.path.join(DISTRACTIONS_DIR, f) for f in os.listdir(DISTRACTIONS_DIR) if f.endswith('.png') or f.endswith('.jpg')]


def get_random_background(min_size=2000, max_size=4000):
    """
    Get a random background image with random dimensions.
    It is randomly a color or an image from the BACKGROUND_DIR.
    """
    shape = np.random.randint(min_size, max_size, size=2)
    if np.random.rand() < 0.3:
        color = np.random.rand(3)
        bg = np.ones((shape[0], shape[1], 3)) * color
        bg = (bg * 255).astype(np.uint8)
        bg = np.clip(bg, 0, 255).astype(np.uint8)
        return bg
    else:
        bg = np.random.choice(background_images)
        bg = plt.imread(bg)
        width_scale = shape[0] / bg.shape[0]
        height_scale = shape[1] / bg.shape[1]
        scale = max(width_scale, height_scale)
        bg = np.resize(bg, (int(bg.shape[0] * scale), int(bg.shape[1] * scale), 3))
        return bg[:shape[0], :shape[1], :3]

def add_random_distractions(img):
    """
    Draws a random number of randomly scaled and rotated distractions on the image.
    """
    num_distractions = np.random.randint(1, 5)
    for _ in range(num_distractions):
        if img.max() <= 1:
            img = (255 * img).astype(np.uint8)
        distraction = np.random.choice(distraction_images)
        distraction_img = plt.imread(distraction)
        if distraction_img.max() <= 1:
            distraction_img = (255 * distraction_img).astype(np.uint8)

        # Randomly scale and rotate the distraction
        size = np.random.uniform(0.05, 0.8) * min(img.shape[0], img.shape[1])
        scale = size / min(distraction_img.shape[0], distraction_img.shape[1])
        angle = np.random.uniform(0, 360)

        # Randomly position the distraction
        x = int(np.random.rand() * (img.shape[1] - size))
        y = int(np.random.rand() * (img.shape[0] - size))

        # Insert the distraction into the image
        img = insert_image(img, distraction_img, x, y, angle, scale)[0]
    return img

#     ---------------------------------------------------------------------------------------------------------------

# background_images_colors = get_random_background()
# bg_with_distractions = add_random_distractions(background_images_colors)
#
# print(len(bg_with_distractions))
# plt.imsave(os.path.join("out","test.png"), bg_with_distractions)

pcb_images = [os.path.join(PCB_DIR, f) for f in os.listdir(PCB_DIR) if f.endswith('.png') or f.endswith('.jpg')]
np.random.shuffle(pcb_images)
print(f"Source PCB images: {len(pcb_images)}")



def create_labeled_sample(pcb_img):
    bg = get_random_background()
    bg_with_distractions = add_random_distractions(bg)

    # Randomly scale and rotate the PCB image, make sure it is always visible
    size = np.random.uniform(0.2, 0.8) * min(bg_with_distractions.shape[0], bg_with_distractions.shape[1])
    scale = size / max(pcb_img.shape[0], pcb_img.shape[1])
    angle = np.random.uniform(0, 360)
    x = int(np.random.rand() * (bg_with_distractions.shape[1] - size))
    y = int(np.random.rand() * (bg_with_distractions.shape[0] - size))
    augmented_img, bounding_box = insert_image(bg_with_distractions, pcb_img, x, y, angle, scale)

    # label format is "class_index x1 y1 x2 y2 x3 y3 x4 y4"
    x1, y1, x2, y2, x3, y3, x4, y4 = bounding_box
    x1 /= augmented_img.shape[1]
    y1 /= augmented_img.shape[0]
    x2 /= augmented_img.shape[1]
    y2 /= augmented_img.shape[0]
    x3 /= augmented_img.shape[1]
    y3 /= augmented_img.shape[0]
    x4 /= augmented_img.shape[1]
    y4 /= augmented_img.shape[0]
    label = f"0 {x1:.6f} {y1:.6f} {x2:.6f} {y2:.6f} {x3:.6f} {y3:.6f} {x4:.6f} {y4:.6f}\n"

    return augmented_img, label, (x1, y1, x2, y2, x3, y3, x4, y4)


OUTPUT_DIR = os.path.join(DATA_DIR, 'augmented')
UPSCALE_FACTOR = 5

for image_path in pcb_images:
    pcb_img = plt.imread(image_path)
    if pcb_img.max() <= 1:
        pcb_img = (255 * pcb_img).astype(np.uint8)

    base_name = os.path.basename(image_path).split('.')[0]
    for i in range(UPSCALE_FACTOR):
        out_path = os.path.join(OUTPUT_DIR, f"{base_name}_{i}.png")
        if os.path.exists(out_path):
            print(f"Skipping {out_path} as it already exists")
            continue

        augmented_img, label, (x1, y1, x2, y2, x3, y3, x4, y4) = create_labeled_sample(pcb_img)
        plt.imsave(os.path.join(OUTPUT_DIR, f"{os.path.basename(image_path).split('.')[0]}_{i}.png"), augmented_img)
