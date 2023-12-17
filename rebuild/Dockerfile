FROM python:3.10.13-slim-bookworm

WORKDIR /app

COPY src .
COPY static_data static_data
COPY reports reports
RUN apt update \
    && apt upgrade -y \
    && apt install gunicorn3 -y \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

CMD ["gunicorn", "--workers=1", "--bind=0.0.0.0", "--timeout=60", "app:app"]
