FROM debian:10.0

MAINTAINER dan.steffen.de@gmail.com

RUN apt-get update -y && \
     apt-get install -y python3 python3-pip uwsgi uwsgi-plugin-python3 

COPY ./requirements.txt wsgi.ini ./wiki.py /opt/wiki/
COPY ./wiki /opt/wiki/wiki

WORKDIR /opt/wiki

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "uwsgi", "--ini", "uwsgi.ini" ]
