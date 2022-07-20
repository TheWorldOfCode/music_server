FROM linuxserver/code-server:focal 

ENV DEBIAN_FRONTED noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

LABEL development="TRUE"

RUN apt update && apt install -y python3 \
                                 python3-pip \
                                 nodejs  \
               && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y build-essential \
                          libpq-dev \
                          telnet \
                          netcat \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
               && rm -rf /var/lib/apt/lists/*

COPY music_server_flask/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN [ -f /usr/bin/python ] && rm /usr/bin/python; \
        ln -s /usr/bin/python3 /usr/bin/python
