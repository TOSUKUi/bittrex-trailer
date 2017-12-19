FROM python:alpine3.6

ADD . /bittrex
WORKDIR /bittrex
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bittrex_observer.py"]
