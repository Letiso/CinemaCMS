FROM python:3.9.9-alpine

ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

RUN apk add --update --no-cache postgresql-client jpeg-dev make gettext
RUN apk update && apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev linux-headers  \
    postgresql-dev musl-dev zlib zlib-dev build-base

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
#RUN apk del .tmp-build-deps

RUN mkdir /cinema
COPY ./cinema /app
WORKDIR /app
