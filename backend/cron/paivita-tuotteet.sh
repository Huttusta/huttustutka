#! /bin/sh

DATA_KANSIO="$1"
KUVAKANSIO="$DATA_KANSIO/kuvat"

/usr/local/bin/python3 ../scripts/get_products.py

cp ../resources/products-sorted.json "$DATA_KANSIO"

/usr/local/bin/python3 ../scripts/get_product_images.py ../resources/products-sorted.json "$KUVAKANSIO"
