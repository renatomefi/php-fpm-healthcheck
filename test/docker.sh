#!/bin/bash

# Author: <Renato Mefi gh@mefi.in> https://github.com/renatomefi
#
# This script is suppose to be ran via Makefile, i.e.:
# $ make test-image DOCKERFILE="alpine" IMAGE="php:7.2-fpm-alpine3.7"
# $ make test-image DOCKERFILE="stretch" IMAGE="php:7.2-fpm-stretch"

set -eEuo pipefail

function cleanup {
docker stop "$CONTAINER" 1> /dev/null
    echo "container $CONTAINER: stopped"
    docker rmi -f "$DOCKER_TAG_TEMPORARY"
}
trap cleanup EXIT

declare -r DOCKER_FILE="$1"
declare -r DOCKER_IMAGE="$2"

declare DOCKER_TAG_TEMPORARY
DOCKER_TAG_TEMPORARY="$DOCKER_IMAGE-$(date +%s)"

sed "s/FROM .*/FROM $DOCKER_IMAGE/g" "./test/Dockerfile-$DOCKER_FILE" | docker build -t "$DOCKER_TAG_TEMPORARY" -f - .

declare CONTAINER
CONTAINER=$(docker run -d --rm "$DOCKER_TAG_TEMPORARY")

declare TESTS_DIR
TESTS_DIR="$(pwd)/test"

docker run --rm -t \
    -v "$TESTS_DIR:/tests" \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    renatomefi/docker-testinfra:latest \
    --verbose --hosts="docker://$CONTAINER" \
    -m "php_fpm or $DOCKER_FILE"
