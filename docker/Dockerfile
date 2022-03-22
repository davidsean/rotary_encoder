FROM arm64v8/ubuntu:latest

LABEL version="0.1"
LABEL David Sean "https://github.com/davidsean"


RUN apt update && apt upgrade -y 
RUN apt install -y locales && locale-gen en_US.UTF-8

RUN DEBIAN_FRONTEND=noninteractive TZ=America/New_York \
    apt install -y python3 pip --no-install-recommends


WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "./docker/entry.sh" ]