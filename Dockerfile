FROM python:3.6

ADD . /bittrex
WORKDIR /bittrex
RUN pip install --no-cache-dir -r requirements.txt
