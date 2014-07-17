Running the test suite
-----------------------

Ensure your PYTHONPATH is set::

	>cd minion/tests
	>cd ..
	>export PYTHONPATH=`pwd`

Run the tests::

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

