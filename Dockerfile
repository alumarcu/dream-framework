FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN pip install pipenv
ADD Pipfile /app/
RUN pipenv install --system

ADD . /app/
