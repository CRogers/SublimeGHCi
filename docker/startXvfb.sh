#!/bin/bash

Xvfb -screen 0 1024x768x24 &>>/dev/null &
ratpoison &>>/dev/null &
x11vnc -display :0 &>>/dev/null &

exit 0