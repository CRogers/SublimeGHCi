#!/bin/bash

echo Running unit tests...
./run_unit_tests.sh
EXIT1=$?
echo Unit tests exited with status $EXIT1

echo
echo Running integ tests....
./run_integ_tests.sh
EXIT2=$?
echo Integ tests exited with status $EXIT2

if [ "$EXIT1" == "0" ] && [ "$EXIT2" == "0" ]; then
        EXIT_STATUS=0
else
        EXIT_STATUS=1
fi

echo
echo Overall exit status: $EXIT_STATUS

exit $EXIT_STATUS