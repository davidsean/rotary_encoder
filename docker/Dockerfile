FROM arm64v8/ubuntu:latest

LABEL version="0.1"
LABEL David Sean "https://github.com/davidsean"


RUN apt update && apt upgrade -y 
RUN apt install -y locales && locale-gen en_US.UTF-8

RUN DEBIAN_FRONTEND=noninteractive TZ=America/New_York \
    apt install -y python3 pip --no-install-recommends

RUN DEBIAN_FRONTEND=noninteractive TZ=America/New_York \
    apt install -y python3-pigpio sudo wget unzip make gcc libc6-dev --no-install-recommends

# consider re-writing the software filter w/out numpy
RUN DEBIAN_FRONTEND=noninteractive TZ=America/New_York \
    apt install -y python3-numpy --no-install-recommends

# PIGPIO
WORKDIR /pigpio
RUN wget https://github.com/joan2937/pigpio/archive/master.zip
RUN  unzip master.zip
WORKDIR /pigpio/pigpio-master

RUN  make
RUN  make install

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "./docker/entry.sh" ]