#! /bin/bash

DATA_KANSIO="$1"

python3 ../scripts/get_products.py

cp ../resources/products-sorted.json "$DATA_KANSIO"
