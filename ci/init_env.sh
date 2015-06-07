#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=dream.settings

# TODO: [ENV-01] Drop database and recreate, remove all migrations and redo them
# TODO: [ENV-02] install fixtures in initenv.

if [ ! -f manage.py ]; then
    echo 'Script should be run from project root dir!'
    exit 1
fi

# Creates the precommit hook symlink
cd .git/hooks/
rm -rf pre-commit
ln -s ../../ci/git_precommit.sh pre-commit

# Back to dreamframework/
cd ../../

echo 'Done!'
exit 0
