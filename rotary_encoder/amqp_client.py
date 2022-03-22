import logging
import os
import json
import pika

from rotary_encoder.rotary_encoder import RotaryEncoder


class AMQPClient:
    """AMQP client class
    """

    AMQP_HOST = os.environ.get('AMQP_HOST')
    AMQP_PORT = os.environ.get('AMQP_PORT')
    USER = os.environ.get('USER')
    PASS = os.environ.get('PASS')

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

        credentials = pika.PlainCredentials(AMQPClient.USER,
                                            AMQPClient.PASS)
        parameters = pika.ConnectionParameters(AMQPClient.AMQP_HOST,
                                               AMQPClient.AMQP_PORT,
                                               '/',
                                               credentials)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rotary_encoder')

        self._push_payload = json.dumps({'cmd': 'push'})
        self._cw_payload = json.dumps({'cmd': 'cw'})
        self._ccw_payload = json.dumps({'cmd': 'ccw'})

        self.rot_enc = RotaryEncoder(push_cback=self._push_cback,
                                     cw_cback=self._cw_cback,
                                     ccw_cback=self._ccw_cback)

        self._logger.info("Instantiation successful")

    def __del__(self) -> None:
        self.connection.close()
        self._logger.info("Instance destroyed")

    def _push_cback(self) -> None:
        self.channel.basic_publish(exchange='',
                                   routing_key='rotary_encoder',
                                   body=self._push_payload)
        self._logger.debug('PUSH msg published to AMQP broker')

    def _cw_cback(self) -> None:
        self.channel.basic_publish(exchange='',
                                   routing_key='rotary_encoder',
                                   body=self._cw_payload)
        self._logger.debug('CW msg published to AMQP broker')

    def _ccw_cback(self) -> None:
        self.channel.basic_publish(exchange='',
                                   routing_key='rotary_encoder',
                                   body=self._ccw_payload)
        self._logger.debug('CCW msg published to AMQP broker')
