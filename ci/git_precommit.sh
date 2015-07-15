#!/bin/sh

echo 'Checking PEP-8...'
exit 1
# Exclude all auto-generated code
pep8 dream/ --exclude="migrations" --max-line-length=99

PEP_CHECK_RESULT=$?

if [ $PEP_CHECK_RESULT -eq 1 ];then
    # Found problems
    exit 1
fi

# Unit tests
echo 'Running unit tests...'

python3 manage.py test

TESTS_OK=$?

if [ $TESTS_OK -eq 1 ];then
    # Found problems
    exit 1
fi


# No errors
echo 'error anyway'
exit 1
