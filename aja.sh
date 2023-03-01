#! /bin/bash

set -o pipefail

BACK_NIMI=
FRONT_NIMI=
SSL_CERTIT_HOSTISSA=/etc/letsencrypt/archive/huttusta.rotta.gt
SSL_CERTIT_KONTISSA=/etc/nginx/certs

while [[ "$1" =~ ^- ]]; do case $1 in
  -h )
    echo "aja.sh [VALITSIMET]"
    echo "Laittaa huttustutkan docker-kuvat ajoon."
    echo
    echo "VALITSIMET:"
    echo "-b <back-nimi> : laita backend ajoon"
    echo "-f <front-nimi> : laita frontend ajoon"
    echo "-h <polku> : ssl-avainten kansio serverillä"
    echo "-k <polku> : ssl-avainten kansio kontissa"
    echo "-h : näytä ohjeet"
    exit
    ;;
  -b )
    shift; BACK_NIMI="$1"
    ;;
  -f )
    shift; FRONT_NIMI="$1"
    ;;
  -h )
    shift; SSL_CERTIT_HOSTISSA="$1"
    ;;
  -k )
    shift; SSL_CERTIT_KONTISSA="$1"
    ;;
esac; shift; done
if [[ "$1" == '-' ]]; then shift; fi

if [[ -n "$BACK_NIMI" ]]; then
  docker rm "$BACK_NIMI" -f && docker run -d --name "$BACK_NIMI" "$BACK_NIMI"
fi

if [[ -n "$FRONT_NIMI" ]]; then
  docker rm "$FRONT_NIMI" -f &&
    docker run -d --name "$FRONT_NIMI" -v "$SSL_CERTIT_HOSTISSA:$SSL_CERTIT_KONTISSA" -p 80:80 -p 443:443 "$FRONT_NIMI"
fi
