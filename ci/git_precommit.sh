#!/bin/sh

echo 'Checking PEP-8...'
# Exclude all auto-generated code
pep8 dream/ --exclude="migrations" --max-line-length=99

PEP_CHECK_RESULT=$?

if [ $PEP_CHECK_RESULT -eq 1 ];then
    # Found problems
    echo 'PEP-8 compliance failed. Fix issues and retry!'
    exit 1
fi

# Unit tests
echo 'Running unit tests...'

python3 manage.py test

TESTS_OK=$?

if [ $TESTS_OK -eq 1 ];then
    # Found problems
    echo 'Unit tests failed. Will not commit!'
    exit 1
fi


# No errors
echo 'Commit OK'
exit 0
