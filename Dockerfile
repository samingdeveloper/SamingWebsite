FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code
WORKDIR /code
COPY . /code/

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#EXPOSE 8000

#ENTRYPOINT ["uwsgi", "--ini", "SamingDev.ini"]

