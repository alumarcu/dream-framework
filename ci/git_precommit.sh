#!/bin/sh

# Exclude all auto-generated code
pep8 dream/ --exclude="migrations" --max-line-length=99

PEP_CHECK_RESULT=$?

if [ $PEP_CHECK_RESULT -eq 1 ];then
    # Found problems
    exit 1
fi

# No errors
exit 0