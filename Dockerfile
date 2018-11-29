FROM python:3.6.5

WORKDIR /app
COPY . /app

EXPOSE 5000

CMD apt-get install python3
RUN apt-get install python3
RUN pip3 install -r requirements.txt
CMD FLASK_APP=alice_app.py flask run --host="::"
