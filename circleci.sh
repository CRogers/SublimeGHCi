#!/bin/bash

echo At location: "$(pwd)"
echo With files: "$(ls)"
docker run -v "$(pwd):/SublimeGHCi" crogers/sublimeghci-docker:latest ./run.sh