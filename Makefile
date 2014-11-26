BASEDIR=$(PWD)
VPYTHON=$(BASEDIR)/tests/ENV/bin/python
export PYTHONPATH=$(BASEDIR)

test:
	$(VPYTHON) tests/test_brain_of_minion.py
