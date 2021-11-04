FROM python:3.8-slim-buster

LABEL maintainer="Loic Tetrel <loic.tetrel.pro@gmail.com>"

#Basic dependencies

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-utils \
        gnupg \
        openssh-server \
        git \
        curl && \
    #git-annex for Datalad following neuro.debian.net/ and github.com/jacobalberty/unifi-docker/issues/64
    curl http://neuro.debian.net/lists/buster.us-nh.full | tee /etc/apt/sources.list.d/neurodebian.sources.list && \
    apt-key adv --keyserver hkps://keyserver.ubuntu.com --recv-keys 0xA5D32F012649A5A9 && \
    apt-get update && \
    apt-get install -y --no-install-recommends git-annex-standalone && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

#python dependencies for Repo2Data and python science databases
RUN mkdir /Repo2Data
WORKDIR /Repo2Data
COPY . /Repo2Data
RUN git config --global user.name "root" && git config --global user.email "root@email.com"
RUN python3 -m pip install --upgrade pip && python3 -m pip install --no-cache \
    scikit-learn==1.0.0 \
    nilearn==0.8.0 && \
    python3 -m pip install --no-cache -e /Repo2Data -r requirements.txt

#data folder for repo2data
RUN mkdir /data
WORKDIR /

ENTRYPOINT ["repo2data"]
CMD ["--server", "-r", "/data/data_requirement.json"]
