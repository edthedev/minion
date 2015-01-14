BASEDIR=$(PWD)
VPYTHON=$(BASEDIR)/ENV/bin/python
VPIP=$(BASEDIR)/ENV/bin/pip
BIN=$(BASEDIR)/ENV/bin
export PYTHONPATH=$(BASEDIR)

env_for_testing:
	virtualenv ENV

requirements_for_testing: env_for_testing
	$(VPIP) install -r tests/requirements.txt

test_brain:
	$(VPYTHON) tests/test_brain_of_minion.py

test_minion:
	$(VPYTHON) tests/test_minion.py

coverage_brain:
	$(BIN)/coverage run --rcfile=tests/coveragerc tests/test_brain_of_minion.py
	$(BIN)/coverage report

coverage_minion:
	$(BIN)/coverage run --rcfile=tests/coveragerc tests/test_minion.py
	$(BIN)/coverage report
