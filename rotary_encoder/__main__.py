import time
from rotary_encoder.amqp_client import AMQPClient

if __name__ == "__main__":
    client = AMQPClient()
    while True:
        time.sleep(1)
