FROM python:3

RUN apt-get update && \
    apt-get upgrade -y && \ 	
    apt-get install -y \
	git \
	build-essential \
	libssl-dev \
	swig \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	nginx \
	supervisor \
	sqlite3 && \
	pip3 install -U pip setuptools && \
   rm -rf /var/lib/apt/lists/*


ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt