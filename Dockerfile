FROM python:3.9.6

COPY . /autoprocess
WORKDIR /autoprocess

# RUN apt-get update && apt-get upgrade \
#     apt-get install -y python3 python3-pip python3-dev build-essential 
#     # && apt-get add --virtual .build-deps g++ python3-dev libffi-dev \
#     # && apt-get add --update python3 \
#     # && pip3 install --upgrade pip setuptools

RUN pip3 install -r requirements.txt 
    # && apt-get delete .build-deps

ENV EMAIL='venueyeonnam@gmail.com'  \
    PASSWORD='yxexkpjdmcqkfedb' \
    NOTION_API_KEY='secret_QGnRiFqCpdqfaTgnkDqbNvffMxpNcwLiJZrBzW9Al6D' \
    DATABASE_ID='d714a888485f406697c049e50977212b' \
    GOOGLE_APPLICATION_CREDENTIALS='/autoprocess/credentials.json'

WORKDIR /autoprocess
ENTRYPOINT ["python3", "app.py"]
