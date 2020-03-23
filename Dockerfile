FROM python:3.7-slim-buster

LABEL maintainer="Loic Tetrel <loic.tetrel.pro@gmail.com>"

#Basic dependencies

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-utils=1.8.2 \
        wget=1.20.1-1.1 \
        gnupg=2.2.12-1+deb10u1 \
        openssh-server=1:7.9p1-10+deb10u2 \
        git=1:2.20.1-2+deb10u1 \
        git-crypt=0.6.0-1 \
        unzip=6.0-23+deb10u1 \
        curl=7.64.0-4+deb10u1 && \
    #git-annex for Datalad following neuro.debian.net/ and github.com/jacobalberty/unifi-docker/issues/64
    wget -O- http://neuro.debian.net/lists/buster.us-nh.full | tee /etc/apt/sources.list.d/neurodebian.sources.list && \
    apt-key adv --recv-keys --keyserver hkp://ipv4.pool.sks-keyservers.net:80 0xA5D32F012649A5A9 && \
    apt-get update && \
    apt-get install -y --no-install-recommends git-annex-standalone && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

#python dependencies for scientific databases
RUN python3 -m pip install --upgrade pip && python3 -m pip install --no-cache \
    scipy==1.2.1 \
    scikit-learn==0.21.1 \
    nilearn==0.6.2

#install repo2data and requirements
RUN mkdir /Repo2Data
WORKDIR /Repo2Data
COPY . /Repo2Data
RUN python3 -m pip install -e /Repo2Data -r requirements.txt

#data folder for repo2data
RUN mkdir /data
WORKDIR /

ENTRYPOINT ["repo2data", "-r", "/data/*.json", "--server"]
