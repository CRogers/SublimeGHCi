cd ..
python3 -m unittest discover -s SublimeGHCi/tests -p *Spec.py
EXIT_STATUS=$?
cd SublimeGHCi

exit $EXIT_STATUS