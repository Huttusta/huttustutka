import PIL
import io
import os
import json
import sys
import requests
from wand.image import Image
from wand.color import Color

OUTPUT_FOLDER = "/home/lauri/projektit/alko_images_transparent_bg"
ALKO_CDN_URL = "https://images.alko.fi/images/cs_srgb,f_auto,t_medium/cdn"
PRODUCTS_JSON = "/home/lauri/projektit/huttustutka/front/src/assets/data/alko_products_available.json"

with open(PRODUCTS_JSON, "r") as f:
    PRODUCTS = json.load(f)

OVERALL = len(PRODUCTS)

# for most products
# BACKGROUND_FADE = 300  # smaller number takes less background

# for very white products
BACKGROUND_FADE = 10  # smaller number takes less background

COLOR = '#FFFFFF'

def run():
    previous = 0
    with requests.Session() as session:
        filtered_products = PRODUCTS
        if len(sys.argv) > 1:
            filtered_products = [p for p in PRODUCTS if p['id'] in sys.argv[1:]]

        for idx, product in enumerate(filtered_products):
            output_file = f"{OUTPUT_FOLDER}/{product['id']}.png"
            if (os.path.exists(output_file)):
                continue

            res = session.get(f"{ALKO_CDN_URL}/{product['id']}/a")
            res.raise_for_status()

            with Image(file=io.BytesIO(res.content)) as img:
                img.format = 'png'
                with Color(COLOR) as white:
                    twenty_percent = BACKGROUND_FADE
                    img.transparent_color(white, alpha=0.0, fuzz=twenty_percent)
                img.save(filename=output_file)

            percent = int(100 * idx / OVERALL)
            if previous < percent:
                print(percent, "% done")
                previous = percent

if __name__ == "__main__":
    run()
