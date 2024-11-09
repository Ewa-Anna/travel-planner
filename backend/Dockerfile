FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

