import time
from rotary_encoder.amqp_client import AMQPClient

if __name__ == "__main__":
    ac = AMQPClient()
    while True:
        time.sleep(1)
