FROM python:3.10

WORKDIR /app

ENV LOCALTIME Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$LOCALTIME /etc/localtime && echo $LOCALTIME > /etc/timezone

COPY . /app

RUN pip3 install -r /app/requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]