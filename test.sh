#!/usr/bin/env bash

TAG="google-domain-ddns-test"
TARGET="test"

source build.sh ${TAG} ${TARGET}

docker run \
    --rm \
	-e DOMAIN="domain.example" \
	-e USERNAME="dummy_username" \
	-e PASSWORD="dummy_password" \
	$TAG \
	--cov=. \
	"${@}"

