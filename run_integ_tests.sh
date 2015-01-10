#!/bin/bash

shopt -s globstar

function kill_dists() {
	echo Killing dists: **/dist/
	rm -rf **/dist/
}

kill_dists

cd ..
python3 -m unittest discover "$1" -s SublimeGHCi/integ_tests -p *IntegSpec.py
EXIT_STATUS=$?
cd SublimeGHCi

kill_dists

exit $EXIT_STATUS