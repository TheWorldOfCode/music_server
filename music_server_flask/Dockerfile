FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONONTWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y build-essential \
                          libpq-dev \
                          telnet \
                          netcat \
                          ffmpeg \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./flask_start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./worker_start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./beat_start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./flower_start /start-celeryflower
RUN sed -i 's/\r$//g' /start-celeryflower
RUN chmod +x /start-celeryflower

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
