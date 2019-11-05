FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python-pip
COPY requirements.txt requirements.txt
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install --yes libgdal-dev
ENV PYTHONPATH $PYTHONPATH:/code
ADD . /code
