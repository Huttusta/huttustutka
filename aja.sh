#! /bin/bash

set -o pipefail

BACK_NIMI=
FRONT_NIMI=
DATA_KANSIO=/opt/huttustutka/data

while [[ "$1" =~ ^- ]]; do case $1 in
  -h )
    echo "aja.sh [VALITSIMET]"
    echo "Laittaa huttustutkan docker-kuvat ajoon."
    echo
    echo "VALITSIMET:"
    echo "-b <back-nimi> : laita backend ajoon"
    echo "-f <front-nimi> : laita frontend ajoon"
    echo "-d <kansio> : absoluuttinen polku datakansioon"
    echo "-h : näytä ohjeet"
    exit
    ;;
  -b )
    shift; BACK_NIMI="$1"
    ;;
  -f )
    shift; FRONT_NIMI="$1"
    ;;
  -d )
    shift; DATA_KANSIO="$1"
    ;;
esac; shift; done
if [[ "$1" == '-' ]]; then shift; fi

if [[ -n "$BACK_NIMI" ]]; then
  docker rm "$BACK_NIMI" -f
  docker run -d --name "$BACK_NIMI" -p 5000:5000 -v "$DATA_KANSIO:$DATA_KANSIO" "$BACK_NIMI"
fi

if [[ -n "$FRONT_NIMI" ]]; then
  docker rm "$FRONT_NIMI" -f
  docker run -d --name "$FRONT_NIMI" -v "/etc/letsencrypt:/etc/letsencrypt" \
    -v "$DATA_KANSIO:$DATA_KANSIO" -p 80:80 -p 443:443 "$FRONT_NIMI"
fi
