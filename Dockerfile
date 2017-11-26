# based on https://github.com/tshirtman/Buildozer-docker

FROM ubuntu:17.04

# Update ubuntu:
RUN apt-get update -qq \
    && apt-get -y full-upgrade \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# install needed packages for buildozer
# https://github.com/kivy/buildozer/blob/master/buildozer/tools/packer/scripts/additional-packages.sh
RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get -y install lib32stdc++6 lib32z1 lib32ncurses5 \
    && apt-get -y install python-pip build-essential \
    && apt-get -y install git openjdk-8-jdk --no-install-recommends zlib1g-dev \
    && pip install -U pip \
    && pip install cython buildozer python-for-android \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install "cython<0.27" \
    && pip install buildozer pyOpenssl

ADD runcalculator /buildozer/runcalculator

RUN adduser buildozer --disabled-password --disabled-login \
    && chown -R buildozer:buildozer /buildozer/

USER buildozer

RUN cd /buildozer/runcalculator \
    && buildozer --verbose android debug \
    && cd .. \
    && rm -rf runcalculator

VOLUME /buildozer/

WORKDIR /buildozer/

CMD buildozer --verbose android release
