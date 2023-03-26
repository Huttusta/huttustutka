#! /bin/bash

set -o pipefail

BACK_NIMI=
FRONT_NIMI=
CRON_NIMI=

while [[ "$1" =~ ^- ]]; do case $1 in
  -h )
    echo "rakenna.sh [VALITSIMET]"
    echo "Rakenna docker kuvat huttustutkasta"
    echo
    echo "VALITSIMET:"
    echo "-b <kuvan-nimi> : rakennetaan backend"
    echo "-f <kuvan-nimi> : rakennetaan frontend"
    echo "-c <kuvan-nimi> : rakennetaan cron"
    echo "-h : näytä ohjeet"
    exit
    ;;
  -b )
    shift; BACK_NIMI="$1"
    ;;
  -f )
    shift; FRONT_NIMI="$1"
    ;;
  -c )
    shift; CRON_NIMI="$1"
    ;;
esac; shift; done
if [[ "$1" == '-' ]]; then shift; fi

if [[ -n "$BACK_NIMI" ]]; then
  docker build backend/ -t "$BACK_NIMI"
fi

if [[ -n "$FRONT_NIMI" ]]; then
  docker build front/ -t "$FRONT_NIMI"
fi

if [[ -n "$CRON_NIMI" ]]; then
  docker build backend/ -t "$CRON_NIMI" -f backend/Dockerfile-cron
fi
