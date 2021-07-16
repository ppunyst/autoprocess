FROM python:3.6.5-alpine

COPY . /autoprocess
WORKDIR /autoprocess

RUN apk update && apk upgrade \
    && apk add --virtual .build-deps g++ python3-dev libffi-dev \
    && apk add --update python3 \
    && pip3 install --upgrade pip setuptools

RUN pip3 install -r requirements.txt \
    && apk del .build-deps

ENV EMAIL='venueyeonnam@gmail.com'  \
    PASSWORD='yxexkpjdmcqkfedb' \
    NOTION_API_KEY='secret_QGnRiFqCpdqfaTgnkDqbNvffMxpNcwLiJZrBzW9Al6D' \
    DATABASE_ID='d714a888485f406697c049e50977212b' \
    GOOGLE_APPLICATION_CREDENTIALS='/autoprocess/credentials.json'

WORKDIR /autoprocess
ENTRYPOINT ["python3", "app.py"]
