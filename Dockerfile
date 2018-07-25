FROM python:3.6.5

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code
WORKDIR /code
COPY . /code/

RUN apt-get update && apt-get install
#RUN apk update && apk add #for alpine based
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#EXPOSE 8000

#ENTRYPOINT ["uwsgi", "--ini", "SamingDev.ini"]

