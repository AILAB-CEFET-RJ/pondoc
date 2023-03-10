FROM python:3.11-slim

WORKDIR /user/app

COPY requirements.txt . 
RUN pip install requirements.txt

COPY source/ . 

RUN rm requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]