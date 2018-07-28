FROM python:3.7.0

#ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code
WORKDIR /code
COPY . /code/

#RUN apt-get update && apt-get install
#RUN apk update && apk add #for alpine based
#RUN pip install --upgrade pip
RUN pip install pytest #&& pip install pytest-timeout

#EXPOSE 8000

#ENTRYPOINT ["uwsgi", "--ini", "SamingDev.ini"]

ENTRYPOINT python ./rt.py #--timeout=2 --tb=line -s