FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/

CMD cd bot_calendario_telegram/ && hug -p 80 -f reminder_rest_api.py

EXPOSE 80
