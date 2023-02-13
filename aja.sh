#! /bin/bash

set -o pipefail

AJA_BACK=false
AJA_FRONT=false
BACK_SISAAN=huttustutka-back.tar
FRONT_SISAAN=huttustutka-front.tar
BACK_NIMI=huttustutka-back
FRONT_NIMI=huttustutka-front
SSL_CERTIT_HOSTISSA=/etc/letsencrypt/archive/huttusta.rotta.gt
SSL_CERTIT_KONTISSA=/etc/nginx/certs

while [[ "$1" =~ ^- ]]; do case $1 in
  -h )
    echo "aja.sh [VALITSIMET]"
    echo "Lataa huttustutkan docker-kuvat tar-tiedostoista ja laittaa ne ajoon."
    echo
    echo "VALITSIMET:"
    echo "-b : ladataan ja ajetaan backend ($BACK_SISAAN)"
    echo "-f : ladataan ja ajetaan frontend ($FRONT_SISAAN)"
    echo "-h <polku> : ssl-avainten kansio serverillä"
    echo "-k <polku> : ssl-avainten kansio kontissa"
    echo "-h : näytä ohjeet"
    exit
    ;;
  -b )
    AJA_BACK=true
    ;;
  -f )
    AJA_FRONT=true
    ;;
  -h )
    shift; SSL_CERTIT_HOSTISSA="$1"
    ;;
  -k )
    shift; SSL_CERTIT_KONTISSA="$1"
    ;;
esac; shift; done
if [[ "$1" == '-' ]]; then shift; fi

if $AJA_BACK; then
  docker load -i "$BACK_SISAAN" && docker rm "$BACK_NIMI" -f &&
    docker run -d --name "$BACK_NIMI" "$BACK_NIMI"
fi

if $AJA_FRONT; then
  docker load -i "$FRONT_SISAAN" && docker rm "$FRONT_NIMI" -f &&
    docker run -d --name "$FRONT_NIMI" -v "$SSL_CERTIT_HOSTISSA:$SSL_CERTIT_KONTISSA" -p 80:80 -p 443:443 "$FRONT_NIMI"
fi
