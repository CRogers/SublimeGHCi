#!/bin/bash

cd ..
python3 -m unittest discover "$1" -s SublimeGHCi/integ_tests -p *IntegSpec.py
EXIT_STATUS=$?
cd SublimeGHCi

exit $EXIT_STATUS