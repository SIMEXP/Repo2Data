FROM python:3.8-buster

LABEL maintainer="Loic Tetrel <loic.tetrel.pro@gmail.com>"

#Basic dependencies
RUN apt-get update; \
    apt-get install -y --no-install-recommends \
    	apt-utils && \
    apt-get install -y --no-install-recommends \    
        openssh-server \
        # git-crypt=0.6.0 \
        # unzip=6.0 \
        # curl=7.58.0 \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#git-annex for Datalad
# https://git-annex.branchable.com/install/ following http://neuro.debian.net/
# RUN wget -O- http://neuro.debian.net/lists/stretch.us-nh.full | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list
# # https://github.com/jacobalberty/unifi-docker/issues/64
# RUN apt-key adv --recv-keys --keyserver hkp://ipv4.pool.sks-keyservers.net:80 0xA5D32F012649A5A9
# RUN apt-get update && \
#     apt-get install -y git-annex-standalone

# #python dependencies for scientific databases
# RUN python3 -m pip install --upgrade pip && python3 -m pip install --no-cache \ 
#     scipy==1.2.1 \
#     scikit-learn==0.21.1 \
#     nilearn==0.6.2

# #install repo2data and requirements
# RUN mkdir /Repo2Data
# COPY . /Repo2Data
# RUN python3 -m pip install -e . -r requirements.txt

# #data folder for repo2data
# RUN mkdir /data
# WORKDIR /data

# CMD ["repo2data"]
