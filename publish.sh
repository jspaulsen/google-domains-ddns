#!/bin/sh

VERSION=$(cat VERSION)
PREFIX="jspaulsen/"
TAG="${1:-"google-domains-ddns"}"
VTAG="${TAG}:v${VERSION}"
TARGET=${2:-base}

BRANCH=$(git symbolic-ref --short -q HEAD)
INCLUDE_LATEST=""

if [ "$BRANCH" = "main" ]; then
    INCLUDE_LATEST="-t ${PREFIX}${TAG}"
else
    echo "Branch is not main; not uploading latest tag"
fi


docker buildx \
    build \
    --push \
    --platform linux/amd64,linux/arm/v7 \
    --target ${TARGET} \
    -t "${PREFIX}${VTAG}" \
    $INCLUDE_LATEST \
    .
