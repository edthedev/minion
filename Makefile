BASEDIR=$(PWD)
VPYTHON=$(BASEDIR)/tests/ENV/bin/python
VPIP=$(BASEDIR)/tests/ENV/bin/pip
export PYTHONPATH=$(BASEDIR)

env:
	virtualenv ENV

requirements:
	$(VPIP) -r requirements.txt


test:
	$(VPYTHON) tests/test_brain_of_minion.py
