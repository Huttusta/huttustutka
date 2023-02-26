#! /bin/bash

set -o pipefail

RAKENNA_BACK=false
RAKENNA_FRONT=false
BACK_ULOS=huttustutka-back.tar
FRONT_ULOS=huttustutka-front.tar
BACK_NIMI=huttustutka-back
FRONT_NIMI=huttustutka-front
OSOITE=
KAYTTAJA=root
KANSIO=/root/
PALVELIN_AJO=aja.sh

while [[ "$1" =~ ^- ]]; do case $1 in
  -h )
    echo "rakenna.sh [VALITSIMET]"
    echo "Rakenna docker kuvat huttustutkasta ja lähetä ja aja ne serverillä"
    echo
    echo "VALITSIMET:"
    echo "-b : rakennetaan backend ($BACK_ULOS)"
    echo "-f : rakennetaan frontend ($FRONT_ULOS)"
    echo "-o <osoite> : serveri jossa kontit ajetaan"
    echo "-k <kayttaja> : käyttäjä serverillä"
    echo "-d <kansio> : kansio serverillä johon kontit siirretään"
    echo "-h : näytä ohjeet"
    exit
    ;;
  -b )
    RAKENNA_BACK=true
    ;;
  -f )
    RAKENNA_FRONT=true
    ;;
  -o )
    shift; OSOITE="$1"
    ;;
  -k )
    shift; KAYTTAJA="$1"
    ;;
  -d )
    shift; KANSIO="$1"
    ;;
esac; shift; done
if [[ "$1" == '-' ]]; then shift; fi

RSYNC_OSOITE="$KAYTTAJA@$OSOITE:$KANSIO"
SSH_OSOITE="$KAYTTAJA@$OSOITE"

if $RAKENNA_BACK; then
  docker build backend/ -t "$BACK_NIMI" && docker save -o "$BACK_ULOS" "$BACK_NIMI" &&
    [[ -n "$OSOITE" ]] && rsync "$BACK_ULOS" "$RSYNC_OSOITE"
fi

if $RAKENNA_FRONT; then
  docker build front/ -t "$FRONT_NIMI" && docker save -o "$FRONT_ULOS" "$FRONT_NIMI" &&
    [[ -n "$OSOITE" ]] && rsync "$FRONT_ULOS" "$RSYNC_OSOITE"
fi

AJA_BACK=
AJA_FRONT=

if $RAKENNA_BACK; then AJA_BACK="-b"; fi
if $RAKENNA_FRONT; then AJA_FRONT="-f"; fi


[[ -n "$OSOITE" ]] && rsync "$PALVELIN_AJO" "$RSYNC_OSOITE" && ssh "$SSH_OSOITE" "./$PALVELIN_AJO $AJA_BACK $AJA_FRONT"
