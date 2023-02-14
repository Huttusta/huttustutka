#! /bin/bash

set -o pipefail

RAKENNA_BACK=false
RAKENNA_FRONT=false
BACK_ULOS=huttustutka-back.tar
FRONT_ULOS=huttustutka-front.tar
BACK_NIMI=huttustutka-back
FRONT_NIMI=huttustutka-front
LAHETA=
PALVELIN_AJO=aja.sh

while [[ "$1" =~ ^- ]]; do case $1 in
  -h )
    echo "rakenna.sh [VALITSIMET]"
    echo "Rakenna docker kuvat huttustutkasta ja tallenna ne tar-tiedostoon."
    echo
    echo "VALITSIMET:"
    echo "-b : rakennetaan backend ($BACK_ULOS)"
    echo "-f : rakennetaan frontend ($FRONT_ULOS)"
    echo "-l <kayttaja>@<osoite>:/kansio/ : lähetä ja aja kontit serverillä"
    echo "-h : näytä ohjeet"
    exit
    ;;
  -b )
    RAKENNA_BACK=true
    ;;
  -f )
    RAKENNA_FRONT=true
    ;;
  -l )
    shift; LAHETA="$1"
    ;;
esac; shift; done
if [[ "$1" == '-' ]]; then shift; fi

if $RAKENNA_BACK; then
  docker build backend/ -t "$BACK_NIMI" && docker save -o "$BACK_ULOS" "$BACK_NIMI" &&
    [[ -n "$LAHETA" ]] && rsync "$BACK_ULOS" "$LAHETA"
fi

if $RAKENNA_FRONT; then
  docker build front/ -t "$FRONT_NIMI" && docker save -o "$FRONT_ULOS" "$FRONT_NIMI" &&
    [[ -n "$LAHETA" ]] && rsync "$FRONT_ULOS" "$LAHETA"
fi

AJA_BACK=
AJA_FRONT=

if $RAKENNA_BACK; then AJA_BACK="-b"; fi
if $RAKENNA_FRONT; then AJA_FRONT="-f"; fi

[[ -n "$LAHETA" ]] && rsync "$PALVELIN_AJO" "$LAHETA" && ssh "${LAHETA%:*}" "./$PALVELIN_AJO $AJA_BACK $AJA_FRONT"
