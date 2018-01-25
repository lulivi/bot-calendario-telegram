FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/

ENV TG_CALENDAR_BOT_TOKEN '450420830:AAFSru7T8O8At7aPRygtlB6NHsH_b8OuEAE'
ENV PORT 80

CMD cd bot_calendario_telegram/ && python reminder_rest_api.py
CMD cd bot_calendario_telegram/ && python bot.py

EXPOSE 80
