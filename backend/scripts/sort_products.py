import json
import sys

PRODUCTS_INPUT = "resources/alko-products.json"
PRODUCTS_OUTPUT = sys.argv[1] + "/products-sorted.json"


def run():
    with open(PRODUCTS_INPUT, "r") as f:
        products = json.load(f)

    products.sort(key=lambda x: x["name"])

    with open(PRODUCTS_OUTPUT, "w") as f:
        json.dump(products, f)


if __name__ == "__main__":
    run()
