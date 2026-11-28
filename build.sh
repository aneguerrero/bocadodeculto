#!/usr/bin/env bash
set -euo pipefail

python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py cargar_demo
python manage.py preparar_roles