BASEDIR=$(PWD)
VPYTHON=$(BASEDIR)/tests/ENV/bin/python
VPIP=$(BASEDIR)/ENV/bin/pip
export PYTHONPATH=$(BASEDIR)

env_for_testing:
	virtualenv ENV

requirements_for_testing: env_for_testing
	$(VPIP) install -r tests/requirements.txt

test_brain:
	$(VPYTHON) tests/test_brain_of_minion.py

test_command_line:
	$(VPYTHON) tests/test_brain_of_minion.py
