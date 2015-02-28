#!/bin/bash
echo "Running tests to confirm basic minion functionality."

minion remind test1 test2
minion count test1 test2
minion find test1 test2
minion list test2
minion sample test2
minion journal testing journal
