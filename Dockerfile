FROM python:latest

WORKDIR /app

COPY source/app . 
RUN apt update \
    && apt upgrade -y \
    && apt install gunicorn3 -y \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["gunicorn", "--workers=1", "--bind=0.0.0.0", "--timeout=300", "app:app"]
