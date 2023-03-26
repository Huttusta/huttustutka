#! /bin/sh

PYTHON_KANSIO="$1"
DATA_KANSIO="$2"

TUOTE_SKRIPTI="$PYTHON_KANSIO/scripts/get_products.py"
KUVA_SKRIPTI="$PYTHON_KANSIO/scripts/get_product_images.py"
TUOTTEET="$PYTHON_KANSIO/resources/products-sorted.json"
KUVAKANSIO="$DATA_KANSIO/kuvat"

/usr/local/bin/python3 "$TUOTE_SKRIPTI"

cp "$TUOTTEET" "$DATA_KANSIO"

/usr/local/bin/python3 "$KUVA_SKRIPTI" "$TUOTTEET" "$KUVAKANSIO"
