# based on https://github.com/D3f0/kivyworkshop/blob/master/docker/Dockerfile

FROM ubuntu:16.04

# Update ubuntu:
RUN apt-get update -qq \
    && apt-get -y full-upgrade \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install buildozer
# https://buildozer.readthedocs.io/en/latest/installation.html#android-on-ubuntu-16-04-64bit
RUN dpkg --add-architecture i386 \
    && apt-get update -qq \
    && apt-get -y install python-pip build-essential ccache git mesa-common-dev libgl1-mesa-dev libncurses5:i386 libstdc++6:i386 libgtk2.0-0:i386 libpangox-1.0-0:i386 libpangoxft-1.0-0:i386 libidn11:i386 python2.7 python2.7-dev openjdk-8-jdk unzip zlib1g-dev zlib1g:i386 \
    && pip install --upgrade pip \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD requirements/*.txt /tmp/

RUN pip install "cython<0.27" \
    && pip install -r /tmp/built.txt

# needs by buildozer
RUN pip install "appdirs" "colorama>=0.3.3" "sh>=1.10,<1.12.5" "jinja2" "six"

# Just use 'user' as username: buildozer doesn't like to run as root

RUN adduser --uid 1000 --disabled-password --gecos "" user \
    && chown -R user /home/user

ADD runcalculator /home/user/runcalculator
RUN chown -R user /home/user/runcalculator \
    && mkdir -p /tmp \
    && chmod 777 -Rf /tmp

WORKDIR /home/user/runcalculator

USER user

RUN ls -la

RUN buildozer android debug
RUN buildozer android release

