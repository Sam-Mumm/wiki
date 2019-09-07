FROM debian:10.0

MAINTAINER dan.steffen.de@gmail.com

RUN apt-get update -y && \
     apt-get install -y python3 python3-pip

COPY ./requirements.txt ./run.py /opt/wiki/
COPY ./app /opt/wiki/app

WORKDIR /opt/wiki

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD ["run.py"]
