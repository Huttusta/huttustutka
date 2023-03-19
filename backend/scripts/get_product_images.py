import io
import os
import json
import sys
import asyncio
import aiohttp
from wand.image import Image
from wand.color import Color

OUTPUT_FOLDER = sys.argv[2] 
ALKO_CDN_URL = "https://images.alko.fi/images/cs_srgb,f_auto,t_medium/cdn"
PRODUCTS_JSON = sys.argv[1] #resources/products-sorted.json
NEW_WIDTH = 100

with open(PRODUCTS_JSON, "r") as f:
    PRODUCTS = json.load(f)

# for most products
BACKGROUND_FADE = 300  # smaller number takes less background

# for very white products
# BACKGROUND_FADE = 10  # smaller number takes less background

COLOR = '#FFFFFF'

async def task(name, work_queue, n_products):
    if work_queue.empty():
        print("Kaikki kuvat ovat käsittelyssä", name)
        return

    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            product_id = await work_queue.get()
            output_file = f"{OUTPUT_FOLDER}/{product_id}.png"

            if os.path.exists(output_file):
                continue

            img = await get_img(product_id, session, name)
            if not img:
                continue

            proccess_img(img, output_file)
            print(n_products - work_queue.qsize(), "/", n_products, "valmis")



async def get_img(product_id, session, name):
    async with session.get(f"{ALKO_CDN_URL}/{product_id}/a") as res:
        if res.status!= 200:
            print(f"Tuotteen {product_id} kuvaa ei voinut ladata {name}")
            return None

        return Image(file=io.BytesIO(await res.read()))


def proccess_img(img, output_file):
    resize_img(img)
    img.transparent_color(Color(COLOR), alpha=0.0, fuzz=BACKGROUND_FADE)
    img.format = 'png'
    img.save(filename=output_file)


def resize_img(img):
    scale = NEW_WIDTH / img.size[0]
    new_size = (int(scale * img.size[0]), int(scale * img.size[1]))
    img.resize(*new_size)


async def run2():
    previous = 0
    work_queue = asyncio.Queue()

    products = [p['id'] for p in PRODUCTS]
    if len(sys.argv) > 1:
        products = [
            p for p in products if p in sys.argv[1:]
        ]

    for work in products:
        await work_queue.put(work)

    n_products = len(products)

    await asyncio.gather(
        asyncio.create_task(task("One", work_queue, n_products)),
        asyncio.create_task(task("Two", work_queue, n_products)),
        asyncio.create_task(task("Three", work_queue, n_products)),
        asyncio.create_task(task("Four", work_queue, n_products)),
    )


if __name__ == "__main__":
    asyncio.run(run2())
