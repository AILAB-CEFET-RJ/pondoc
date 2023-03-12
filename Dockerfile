FROM python:3.10-slim

ENV YEAR = ${YEAR}
ENV FILE = ${FILE}

RUN echo $YEAR

WORKDIR /user/app

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY source/ . 

RUN rm requirements.txt

RUN ls

ENTRYPOINT [ "python3" ]
CMD [ "main.py", "-y", "$YEAR", "-f", "$FILE" ]