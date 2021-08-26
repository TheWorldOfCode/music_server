FROM ubuntu:latest

ENV DEBIAN_FRONTED noninteractive

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Setting timezone 
ENV TZ=Europe/Copenhagen
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


LABEL maintainer TheWorldOfCode
LABEL version 0.0.1

RUN apt update && apt install -y mpd \
                                 python3 \
                                 build-essential \
                                 python3-pip \
                                 ffmpeg \
               && rm -rf /var/lib/apt/lists/*


# Install python packages
RUN ln -s /usr/bin/python3 /usr/bin/python


ADD requirements.txt /tmp/
RUN python -m pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

RUN mkdir /data; mkdir app; mkdir config

RUN rm /etc/mpd.conf && ln -s /config/mpd.conf /etc/mpd.conf

COPY web /app
VOLUME ["/data", "/config"]

RUN mkdir /run/mpd
ADD /init /
ENTRYPOINT ["/init"] 


# vim: filetype=dockerfile
