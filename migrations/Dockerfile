FROM python:3.12-alpine3.19

ARG APP_PATH=/opt
ARG UNAME=www
ARG UID=1000

WORKDIR $APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

COPY ./migrations/req.txt $APP_PATH/migrations/req.txt
#COPY ./src $APP_PATH/src
COPY alembic.ini $APP_PATH/alembic.ini

RUN pip install --no-cache-dir --upgrade -r $APP_PATH/migrations/req.txt && \
    adduser -u $UID -s /bin/bash -D -S $UNAME
USER $UNAME