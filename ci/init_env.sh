#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=dream.settings

# TODO: [ENV-01] Drop database and recreate, remove all migrations and redo them
# TODO: [ENV-02] install fixtures in initenv

# Creates the precommit hook symlink
ln -s git_precommit.sh ../.git/hooks/pre-commit