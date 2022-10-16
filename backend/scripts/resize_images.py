import os
from PIL import Image


IMAGES_INPUT_FOLDER = "/home/lauri/projektit/alko_images_transparent_bg/"
IMAGES_OUTPUT_FOLDER = "/home/lauri/projektit/alko_images_small/"
NEW_WIDTH = 100

def run():
    files = os.listdir(IMAGES_INPUT_FOLDER)
    overall = len(files)
    for idx, file in enumerate(files):
        img = Image.open(f"{IMAGES_INPUT_FOLDER}{file}")
        scale = NEW_WIDTH / img.size[0]
        new_size = (int(scale * img.size[0]), int(scale * img.size[1]))
        new_img = img.resize(new_size)
        new_img.save(f"{IMAGES_OUTPUT_FOLDER}{file}")
        print((idx + 1), "/", overall, "valmis")


if __name__ == "__main__":
    run()
