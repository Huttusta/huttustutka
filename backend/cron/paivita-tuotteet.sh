#! /bin/bash

TYOKANSIO="$1"
DATA_KANSIO="$2"

cd "$TYOKANSIO"

if [ ! -d "venv" ]; then
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
else
  source venv/bin/activate
fi

python3 scripts/get_products.py

cp resources/products-sorted.json "$DATA_KANSIO"
