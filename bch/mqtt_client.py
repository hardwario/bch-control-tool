import paho.mqtt.client
from paho.mqtt.client import topic_matches_sub
import logging
import simplejson as json
import time


class MqttClient:

    def __init__(self, host, port, username=None, password=None, cafile=None, certfile=None, keyfile=None):
        port = int(port)

        self.mqttc = paho.mqtt.client.Client()
        self.mqttc.on_connect = self._mqtt_on_connect
        self.mqttc.on_message = self._mqtt_on_message
        self.mqttc.on_disconnect = self._mqtt_on_disconnect

        self.on_message = None

        if username:
            self.mqttc.username_pw_set(username, password)

        if cafile:
            self.mqttc.tls_set(cafile, certfile, keyfile)

        logging.info('MQTT broker host: %s, port: %d, use tls: %s', host, port, bool(cafile))

        self.mqttc.connect(host, port, keepalive=10)

        self._response_condition = 0
        self._response_topic = None
        self._response = None

        self._loop_start = False

    def loop_start(self):
        if self._loop_start:
            return

        self._loop_start = True
        self.mqttc.loop_start()

    def loop_forever(self):
        self.mqttc.loop_forever()

    def _mqtt_on_connect(self, client, userdata, flags, rc):
        logging.info('Connected to MQTT broker with code %s', rc)

        lut = {paho.mqtt.client.CONNACK_REFUSED_PROTOCOL_VERSION: 'incorrect protocol version',
               paho.mqtt.client.CONNACK_REFUSED_IDENTIFIER_REJECTED: 'invalid client identifier',
               paho.mqtt.client.CONNACK_REFUSED_SERVER_UNAVAILABLE: 'server unavailable',
               paho.mqtt.client.CONNACK_REFUSED_BAD_USERNAME_PASSWORD: 'bad username or password',
               paho.mqtt.client.CONNACK_REFUSED_NOT_AUTHORIZED: 'not authorised'}

        if rc != paho.mqtt.client.CONNACK_ACCEPTED:
            logging.error('Connection refused from reason: %s', lut.get(rc, 'unknown code'))

        if rc == paho.mqtt.client.CONNACK_ACCEPTED:
            pass

    def _mqtt_on_disconnect(self, client, userdata, rc):
        logging.info('Disconnect from MQTT broker with code %s', rc)

    def _mqtt_on_message(self, client, userdata, message):
        logging.debug('mqtt_on_message %s %s', message.topic, message.payload)

        payload = message.payload.decode('utf-8')

        try:
            payload = json.loads(payload, use_decimal=True)
        except Exception as e:
            raise
            logging.error(e)

        if self.on_message:
            self.on_message(self, message.topic, payload)

        if self._response_topic and topic_matches_sub(self._response_topic, message.topic):

            response = {"payload": payload, "topic": message.topic}

            if self._response_list:
                if not self._response:
                    self._response = []
                self._response.append(response)

            else:

                self._response = response
                self._response_condition = 0

    def publish(self, topic, payload=None, qos=1):
        self.loop_start()
        if isinstance(topic, list):
            topic = '/'.join(topic)
        return self.mqttc.publish(topic, json.dumps(payload, use_decimal=True), qos=qos)

    def subscribe(self, topic):
        self.mqttc.subscribe(topic)

    def command(self, request_topic, request_payload, response_topic=None, response_list=None, timeout=1):
        self.loop_start()

        if isinstance(request_topic, list):
            request_topic = '/'.join(request_topic)

        if response_topic:
            if isinstance(response_topic, list):
                response_topic = '/'.join(response_topic)

            self.mqttc.subscribe(response_topic)
            self._response_topic = response_topic
            self._response = None
            self._response_list = response_list

        msq = self.mqttc.publish(request_topic, json.dumps(request_payload, use_decimal=True), qos=1)

        if response_topic:
            msq.wait_for_publish()
            self._response_condition = time.time() + timeout
            while self._response_condition > time.time():
                time.sleep(0.001)

        self._response_topic = None
        return self._response

    def gateway_list(self):
        print(self.command("gateway/all/info/get", None, "gateway/+/info", response_list=True))
        print(self.command("gateway/usb-dongle/nodes/get", None, "gateway/usb-dongle/nodes"))
