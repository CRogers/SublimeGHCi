#!/bin/bash

python3 -m unittest discover "$1" -s integ_tests -p *IntegSpec.py