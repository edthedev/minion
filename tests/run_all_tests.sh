#! /bin/bash -e
source ENV/bin/activate
cd ..
export PYTHONPATH=`pwd`
cd tests
python test_brain_of_minion.py
