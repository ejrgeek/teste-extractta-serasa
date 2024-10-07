#!/bin/sh


set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Configurando Banco de Dados ($POSTGRES_HOST $POSTGRES_PORT)"
  sleep 2
done

echo "✅ Banco de Dados Iniciado ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000