#! /bin/bash

TYOKANSIO="$1"
DATA_KANSIO="$2"

cd "$TYOKANSIO"

python3 scripts/get_products.py

cp resources/products-sorted.json "$DATA_KANSIO"
