FROM appropriate/curl:latest

RUN apk update && apk add --no-cache docker
RUN mkdir -p /backups/
ADD cron2/crontab.txt /crontab.txt
ADD cron2/script.sh /script.sh
COPY cron2/entry.sh /entry.sh
RUN chmod 755 /script.sh /entry.sh
RUN /usr/bin/crontab /crontab.txt

CMD ["/entry.sh"]