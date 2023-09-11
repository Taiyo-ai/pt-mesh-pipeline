FROM python:3.8-slim-buster

COPY . .

RUN pip3 install --default-timeout=1000 -r requirements.txt

ENTRYPOINT ["python3"]
