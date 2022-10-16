import io
import os
import json
import sys
import asyncio
import aiohttp
from wand.image import Image
from wand.color import Color

OUTPUT_FOLDER = "/home/lauri/projektit/alko_images_transparent_bg"
ALKO_CDN_URL = "https://images.alko.fi/images/cs_srgb,f_auto,t_medium/cdn"
PRODUCTS_JSON = "/home/lauri/projektit/huttustutka/backend/resources/products-sorted.json"

with open(PRODUCTS_JSON, "r") as f:
    PRODUCTS = json.load(f)

# OVERALL = len(PRODUCTS)

# for most products
# BACKGROUND_FADE = 300  # smaller number takes less background

# for very white products
BACKGROUND_FADE = 10  # smaller number takes less background

COLOR = '#FFFFFF'

async def task(name, work_queue, n_products, previous):
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
            previous = percent(
                n_products,
                work_queue.qsize(),
                previous,
                name,
            )


async def get_img(product_id, session, name):
    async with session.get(f"{ALKO_CDN_URL}/{product_id}/a") as res:
        if res.status!= 200:
            print(f"Tuotteen {product_id} kuvaa ei voinut ladata {name}")
            return None

        return Image(file=io.BytesIO(await res.read()))


def proccess_img(img, output_file):
    img.format = 'png'
    img.transparent_color(Color(COLOR), alpha=0.0, fuzz=BACKGROUND_FADE)
    img.save(filename=output_file)


def percent(n_products, left, previous, name):
    percent = int(100 * (n_products - left) / n_products)
    if previous < percent:
        print(percent, "% done", name)
        return percent
    return previous


async def run2():
    previous = 0
    work_queue = asyncio.Queue()

    filtered_products = [p['id'] for p in PRODUCTS]
    if len(sys.argv) > 1:
        filtered_products = [
            p for p in PRODUCTS if p['id'] in sys.argv[1:]
        ]

    for work in filtered_products:
        await work_queue.put(work)

    n_products = len(filtered_products)

    await asyncio.gather(
        asyncio.create_task(task("One", work_queue, n_products, previous)),
        asyncio.create_task(task("Two", work_queue, n_products, previous)),
        asyncio.create_task(task("Three", work_queue, n_products, previous)),
        asyncio.create_task(task("Four", work_queue, n_products, previous)),
    )


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

            if res.status_code != 200:
                print(f"Tuotteen {product['id']} kuvaa ei voinut ladata")
                continue

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
    asyncio.run(run2())
