# Teste - Brain Agriculture
Backend em Python/Django

### Setup:
Requisitos -> dev:
* Python 3.10+
* SQLite3

Requisitos -> homol:
* Python 3.10+
* PostgreSQL 14.5+

Requisitos -> prod:
* Python 3.10+
* DEFINIR

( Homol) Recomendação - configurando o PostgreSQL (mude nome do banco, nome do usuário e senha):

    sudo -i -u postgres psql
    CREATE DATABASE nome_do_banco;
    CREATE USER nome_usuario WITH PASSWORD 'sua_senha';
    ALTER ROLE nome_usuario SET client_encoding TO 'utf8';
    ALTER ROLE nome_usuario SET default_transaction_isolation TO 'read committed';
    ALTER ROLE nome_usuario SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE nome_do_banco TO nome_usuario;
    
Agora você precisa clonar o repositório

    git clone https://github.com/ejrgeek/teste-extractta-serasa

Depois caso queira, pode criar um novo ambiente virtual para rodar a aplicação, você pode ler aqui para saber mais caso não tenha conhecimento sobre: https://pythonacademy.com.br/blog/python-e-virtualenv-como-programar-em-ambientes-virtuais

Depois de criado, você entra no ambiente e roda os comandos

    pip install -r requirements-dev.txt

Agora vá no arquivo *core/settings/homol.py* e altere o bloco de acordo com os dados que você criou anteriormente ou altere o arquivo *.env*:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": config("HOMOL_DATABASE_NAME"),
            "USER": config("HOMOL_DATABASE_USERNAME"),
            "PASSWORD": config("HOMOL_DATABASE_PASSWORD"),
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }


É necessário configurar as variáveis de ambiente, siga o exemplo do arquivo *.env-sample* e crie um arquivo *.env* atribuindo os valores informados pelo engenheiro responsável. Exemplo do arquivo:
```
SECRET_KEY=
ENV=dev
DEBUG=True

# ADDRS
ALLOWED_HOSTS=*,
INTERNAL_IPS=127.0.0.1,localhost,0.0.0.0
CORS_ORIGIN_WHITELIST=http://localhost,http://localhost:3000,http://127.0.0.1:3000
ALLOWED_CORS_ORIGIN_HOSTS=http://localhost,http://localhost:3000,http://127.0.0.1:3000

# HOMOL DATABASE
HOMOL_DATABASE_NAME=
HOMOL_DATABASE_USERNAME=
HOMOL_DATABASE_PASSWORD=

# SMTP SETTINGS
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = 
EMAIL_PORT = 
EMAIL_HOST_USER = 
EMAIL_HOST_PASSWORD = 
DEFAULT_FROM_EMAIL = 

# REDIS-CELERY SETTINGS
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = {'application/json'}
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Fortaleza'
CELERY_RESULT_BACKEND = 'django-db'

# SENTRY KEY
SENTRY_KEY=https://5a93634249424baba81e33705e51fb44@o4504045995491328.ingest.sentry.io/4504045998702592

# REDIS
REDIS=redis://redis:6379/0

# APP VERSION
VERSION=0.0.1+build-setup
```


Pronto, agora rode os comandos para fazer a migração das tabelas do banco de dados baseados nos Models do Django gerado pelo ORM.:

    python manage.py makemigrations
    python manage.py migrate
    

Depois você pode rodar o comando para criar um super usuario:
    
    python manage.py createsuperuser

Você também precisa pré-cadastrar alguns dados, rode:
    
    python manage.py COMANDO

Depois você pode rodar um:

    python manage.py runserver localhost:8000
    
A aplicação está no ar (localmente pelo menos rs). Ainda é necessário algumas configurações.

Link do Postman com os consumos da API:

    LINK

Caso você deseje fazer consumo da Api, pesque no arquivo *core/settings/base.py* a lista **CORS_ORIGIN_WHITELIST** e adicione o endereço:porta na lista para não ter problemas.


<h4 style="color: red;"><strong>INDISPONÍVEL NO MOMENTO</strong></h4>

    Para os testes nos models você precisa usar um token válido, foi utilizado o [Faker](https://faker.readthedocs.io/en/master/) para gerar dados fictícios, TestCase do Django. Para rodar os testes, use o comando *python manage.py test*.
