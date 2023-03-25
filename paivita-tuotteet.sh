TUOTTEET_TIEDOSTO="$1"

cd backend/

if [ ! -d "venv" ]; then
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
else
  source venv/bin/activate
fi

python3 scripts/get_products.py "$TUOTTEET_TIEDOSTO"
