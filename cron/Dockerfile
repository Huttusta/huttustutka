FROM alpine:3.6

COPY cronjobs /opt/huttustutka/cronjobs
RUN crontab /opt/huttustutka/cronjobs

# start crond with log level 8 in foreground, output to stderr
CMD ["crond", "-f", "-d", "8"]
