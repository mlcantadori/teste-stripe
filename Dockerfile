# pull official base image
FROM python:3.8.0-alpine

ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir /code
WORKDIR /code

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy project
COPY . /code/
