#!/bin/bash
CONTAINER="siu"
DIRECTORY="/root"

while getopts "c:d:" option; do
  case $option in
    c ) CONTAINER=$OPTARG
    ;;
    d ) DIRECTORY=$OPTARG
    ;;
  esac
done

if [[ -z "$CONTAINER" || -z "$DIRECTORY" ]]; then #if no file specified
    yell() { echo "$0: $*" >&2; }
    die() { yell "$*"; exit 111; }
    try() { "$@" || die "cannot $*"; }
fi

docker cp $DIRECTORY/. $CONTAINER:root/$DIRECTORY/