FROM python:3.9.10-alpine3.14
WORKDIR /usr/src/app
ENV FLASK_APP=app
COPY /app/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt