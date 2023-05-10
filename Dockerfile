FROM python:latest

WORKDIR /user/app

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY source/ . 

RUN rm requirements.txt

CMD ["python3", "-m", "flask", "--app", "app/app.py", "run", "--host=0.0.0.0"]