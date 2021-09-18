#!/usr/bin/env bash

VERSION=$(cat VERSION)
TAG="${1:-"google-domains-ddns"}"
VTAG="${TAG}:v${VERSION}"
TARGET=${2:-base}


docker buildx \
    build \
    --platform linux/amd64,linux/arm/v7 \
    --target ${TARGET} \
    -t "${TAG}" \
    -t "${VTAG}" \
    .

# docker build \
#     -t "${TAG}" \
#     -t "${VTAG}" \
#     --target ${TARGET} \
#     .


# docker buildx create --platform linux/amd64,linux/arm/v5 --use
# linux/arm/v5
# docker run --privileged --rm tonistiigi/binfmt:qemu-v5.2.0 --install all
