#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=dream.settings

# TODO: [ENV-01] Drop database and recreate, remove all migrations and redo them
# TODO: [ENV-02] install fixtures in initenv.
# TODO: [ENV-03] Check that all dependencies are installed (python version, pep8, etc.)

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

# Django migrations
python3 manage.py makemigrations
python3 manage.py migrate auth
python3 manage.py migrate

# TODO: [ENV-01] Make sure migrations are correctly applied
# TODO: [ENV-02] Add two test teams into fixtures

# Install fixtures to dreamframework db
psql -U postgres -d dreamframework -a -f docs/sql/fixtures.sql

echo 'Done!'
exit 0
