FROM python:3.7

RUN apt-get update

RUN mkdir -p /workdir
WORKDIR /workdir

RUN git clone https://github.com/samtools/htslib