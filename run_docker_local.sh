#!/bin/bash

docker run -it -v "$(pwd):/SublimeGHCi" -p 5900:5900 99ca51da5c01 "$@"