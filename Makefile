BASEDIR=$(PWD)
VPYTHON=$(BASEDIR)/ENV/bin/python
export PYTHONPATH=$(BASEDIR)

test:
	python tests/test_brain_of_minion.py
