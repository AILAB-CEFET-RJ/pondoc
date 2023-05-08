FROM python:latest

RUN set -x \
    && apt update \
    && apt upgrade -y \
    && apt install -y cron \
    && apt autoremove -y

COPY docker/cron/cron.d/app /etc/cron.d/app
RUN chmod 0644 /etc/cron.d/app \
    && crontab /etc/cron.d/app \
    && mkdir -p /var/log/cron \
    && touch /var/log/cron/app.log

WORKDIR /app

COPY requirements.txt . 
RUN pip install -r requirements.txt
RUN rm requirements.txt

CMD cron && tail -f /var/log/cron/app.log