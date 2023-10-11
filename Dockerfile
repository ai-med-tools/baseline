FROM python:3.10

WORKDIR /app

ENV LOCALTIME Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$LOCALTIME /etc/localtime && echo $LOCALTIME > /etc/timezone

RUN set -ex && \
	mkdir -p /app/files /app/logs /app/tmp


COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
COPY ./baseline.py ./
COPY ./test.py ./
COPY ./baseline_constants.py ./
COPY ./cfg_support.py ./
COPY ./core.py ./
COPY ./log.py ./
COPY ./namespace_logic.py ./
COPY ./utils.py ./
COPY ./validator.py ./

COPY files /app/files
COPY logs /app/logs
COPY tmp /app/tmp


ENTRYPOINT ["python","./test.py"]