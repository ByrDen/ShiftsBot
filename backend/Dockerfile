FROM python:3.12-alpine3.19

ARG APP_PATH=/opt
ARG UNAME=www
ARG UID=1000

WORKDIR $APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

COPY ./backend/req.txt $APP_PATH/backend/req.txt
#COPY ./bot $APP_PATH/bot
#COPY ./src $APP_PATH/src

RUN pip install --no-cache-dir --upgrade -r $APP_PATH/backend/req.txt && \
    adduser -u $UID -s /bin/bash -D -S $UNAME
USER $UNAME