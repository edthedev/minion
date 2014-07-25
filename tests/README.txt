Running the test suite
-----------------------

Setup a test environment::

    >sudo pip install virtualenv
    >cd minion/tests
    >virtualenv ENV


Activate the environment.

    >source ENV/bin/activate
    >pip install -r requirements.txt

Ensure your PYTHONPATH is set::

	>cd minion/tests
	>cd ..
	>export PYTHONPATH=`pwd`

Optionally you can add a line to minion/test/ENV/bin/activate to set your PYTHONPATH automatically, next time::
    
    # If you installed in your home directory
    export PYTHONPATH="~/minion"
    # or if you installed with Vundle
    export PYTHONPATH="~/.vim/bundle/minion"

Run the tests::

    >pip install mock
    >cd minion/tests
    >python test_brain_of_minion.py

Testing the test suite's coverage
----------------------------------
Install coverage::

    >pip install coverage

Run coverage::

    >coverage run test_brain_of_minion.py

Display coverage results::

    >coverage report
    Name                                               Stmts   Miss  Cover
    ----------------------------------------------------------------------
    /Library/Python/2.7/site-packages/mock              1249    668    47%
    /Users/edward/.vim/bundle/minion/brain_of_minion    1082    883    18%
    test_brain_of_minion                                  41      0   100%
    ----------------------------------------------------------------------
    TOTAL                                               2372   1551    35%

Get a nice HTML view::

    >coverage html
    ># For Mac users:
    >open htmlcov/index.html
    ># For Linux users:
    >firefox htmlcov/index.html

