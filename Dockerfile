FROM python:3.11-slim

ARG YEAR
ARG FILE
ENV YEAR = ${YEAR}
ENV FILE = ${FILE}

RUN echo $YEAR

WORKDIR /user/app

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY source/ . 

RUN rm requirements.txt

CMD python3 main.py -y $YEAR -f $FILE