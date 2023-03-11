FROM python:3.11.1-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade cython && pip install --upgrade pip
RUN pip install -r ./requirements.txt