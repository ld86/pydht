FROM python:2.7
MAINTAINER Bogdan Melnik <teh.ld86@gmail.com>

RUN apt-get update
RUN apt-get -y upgrade

RUN git clone https://github.com/ld86/pydht.git
RUN pip install flask

CMD python pydht/dht.py
