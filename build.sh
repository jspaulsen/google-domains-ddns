#!/usr/bin/env bash

VERSION=$(cat VERSION)
TAG="${1:-"google-domains-ddns"}"
VTAG="${TAG}:v${VERSION}"
TARGET=${2:-base}


docker build \
    -t "${TAG}" \
    -t "${VTAG}" \
    --target ${TARGET} \
    .
