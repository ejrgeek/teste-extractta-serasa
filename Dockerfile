FROM python:3.12.7-alpine3.20
LABEL mantainer="ejrflaut@hotmail.com"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY project /project
COPY scripts /scripts

WORKDIR /project

EXPOSE 8000


RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip setuptools && \
  /venv/bin/pip install -r /project/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts


ENV PATH="/scripts:/venv/bin:$PATH"


USER duser


CMD ["commands.sh"]