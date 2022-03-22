#!/bin/bash

# wait for rabbitmq container
./docker/wfi.sh -h rabbitmq -p 5672 -t 30

# start the deamon
sudo pigpiod

python3 -m rotary_encoder