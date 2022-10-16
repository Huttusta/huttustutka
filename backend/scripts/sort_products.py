import json


PRODUCTS_INPUT = "resources/products-2022-10-15 02:21:25.212684.json"
PRODUCTS_OUTPUT = "resources/products-sorted.json"


def run():
    with open(PRODUCTS_INPUT, "r") as f:
        products = json.load(f)

    products.sort(key=lambda x: x["name"])

    with open(PRODUCTS_OUTPUT, "w") as f:
        json.dump(products, f)


if __name__ == "__main__":
    run()
