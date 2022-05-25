#!/bin/bash
CONTAINER="siu"
FILE=""
CONTAINER_DIRECTORY="/root"

while getopts "c:f:d:" option; do
  case $option in
    c ) CONTAINER=$OPTARG
    ;;
    f ) FILE=$OPTARG
    ;;
    d ) CONTAINER_DIRECTORY=$OPTARG
    ;;
  esac
done

if [[ -z "$FILE" || -z "$CONTAINER" || -z "$CONTAINER_DIRECTORY" ]]; then #if no file specified
    yell() { echo "$0: $*" >&2; }
    die() { yell "$*"; exit 111; }
    try() { "$@" || die "cannot $*"; }
fi

docker exec $CONTAINER bash -c "source /root/siu_ws/devel/setup.bash && python3 $CONTAINER_DIRECTORY/$FILE"