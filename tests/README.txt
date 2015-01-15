About this Guide
-----------------
This is the guide to setup and run the test suite for Minion.
All of the relevant exectuable commands are in Makefile.

The steps in this guide assume that you have Python, VirtualEnv, and Make installed.

If you don't want to install make, simply run the commands in the Makefile anywhere they are referenced below.

This guide only references the make commands because they are easier to type, and they are unlikely to change. The commands in the Makefile require more typing, and may improved from time to time.

Setup for Testing
------------------
Run the following to install the requirements for testing::

    # cd <<minion root>>
    make requirements_for_testing

Running Tests
--------------
To run the test suite::

    # cd <<minion root>>
    make test

To see a coverage report::

    # cd <<minion root>>
    make coverage
    make html_coverage

Core functions::
    
    Create a note
    Find a note
    Handle collisions gracefully

Running the test suite
-----------------------

Setup a test environment::

    >sudo pip install virtualenv
    >cd minion/tests
    >virtualenv ENV

Activate the environment.::

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

    >cd minion/tests
    >python test_brain_of_minion.py

Once you've done the above steps, you can run the test suite with::

    >cd minion/tests
    ./run_all_tests.sh


Testing the test suite's coverage
----------------------------------
Install coverage::
    
    # If you're using VirtualEnv, this was done earlier.
    >pip install coverage

Run coverage::
    
    >coverage run --rcfile=coveragerc test_brain_of_minion.py

Note: Using --rcfile=coveragerc prevents testing external dependecies such as Mock.

Display coverage results::

    >coverage report 

Get a nice HTML view::

    >coverage html
    ># For Mac users:
    >open htmlcov/index.html
    ># For Linux users:
    >firefox htmlcov/index.html

