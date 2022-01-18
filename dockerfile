FROM python:3.10-slim

ENV DEBIAN_FRONTED noninteractive

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Setting timezone 
ENV TZ=Europe/Copenhagen
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


LABEL maintainer TheWorldOfCode
LABEL version 0.0.1

RUN pip install --no-cache-dir flask python-mpd2 youtube-dl youtube-search-python music-tag pydub
RUN apt update && apt install -y sqlite3 \
              && rm -rf /var/lib/apt/lists/*

COPY ./web /app
VOLUME ["/app/static/music"]
WORKDIR "/app"
CMD ["main.py"]
ENTRYPOINT ["python3"]

# vim: filetype=dockerfile
