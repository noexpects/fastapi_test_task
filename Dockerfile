FROM python:3.8
WORKDIR /usr/src/user_api
COPY ./app ./app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
