#!/bin/bash

CACHE_DIR="$HOME/docker"
IMAGE="$CACHE_DIR/image.tar"
DOCKER_TAG=crogers/sublimeghci-docker:latest

mkdir -p $CACHE_DIR
if [[ -e $IMAGE ]]; then
	echo Loading docker image...
	docker load -i $IMAGE
else
	echo FROM $DOCKER_TAG >Dockerfile
	echo Downloading docker layers...
	docker build -t $DOCKER_TAG .
	echo Saving docker image...
	docker save $DOCKER_TAG >$IMAGE
fi