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
