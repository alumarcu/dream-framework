#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=dream.settings

# TODO: [ENV-01] Drop database and recreate, remove all migrations and redo them
# TODO: [ENV-02] install fixtures in initenv.
# TODO: [ENV-03] Check that all dependencies are installed (python version, pep8, etc.)

if [ ! -f manage.py ]; then
    echo 'Script should be run from project root dir! (same level with manage.py)'
    exit 1
fi

# Check python exists
python3_missing='python3 binary is missing from your system!'
command -v python3 >/dev/null 2>&1 || { echo $python3_missing; exit 1; }

# Check django version
django_version=`python3 -c "import django; print(django.get_version())"`
ver_maj=`echo "$django_version" | cut -d'.' -f 1`
ver_min=`echo "$django_version" | cut -d'.' -f 2`
ver_min_ok=`echo $(($ver_min > 7))`

if [ ! "$ver_maj" -eq 1 ] || [ ! "$ver_min_ok" -eq 1 ]; then
    echo 'Minimum required version of Django is 1.8!'
    exit 1
fi

# Creates the precommit hook symlink
cd .git/hooks/
rm -rf pre-commit
ln -s ../../ci/git_precommit.sh pre-commit

# Back to dreamframework/
cd ../../

# Database
read -p "Can I drop/recreate dreamframework database, redo migrations, install fixtures? [yN]" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'dreamframework'"
    drop=`psql -U postgres -c "DROP DATABASE IF EXISTS dreamframework"`
    if [ "$drop" == "DROP DATABASE" ]; then
        psql -U postgres -c "CREATE DATABASE dreamframework"
        echo 'Drop/create OK!'
        echo '------------------------------------------------------------------'

        # Django migrations
        rm -rf ./dream/core/migrations
        rm -rf ./dream/engine/soccer/migrations

        python3 manage.py makemigrations
        python3 manage.py migrate auth
        python3 manage.py migrate
        echo 'Django migrations OK!'
        echo '------------------------------------------------------------------'

        # Create Superuser
        python3 manage.py createsuperuser
        echo 'Superuser created OK!'
        echo '------------------------------------------------------------------'

        # Install fixtures to dreamframework db
        psql -U postgres -d dreamframework -q -f docs/sql/fixtures.sql
        echo 'Fixtures installed OK!'
        echo '------------------------------------------------------------------'
    fi
fi

chmod 775 ./ci/init_env.sh
echo 'Done!'
exit 0
