#!/usr/bin/env python3
import os
import sys
import time
import logging
import simplejson as json
import platform
import decimal
import paho.mqtt.client
from paho.mqtt.client import topic_matches_sub

mqtt_connect_rc_lut = {
    paho.mqtt.client.CONNACK_REFUSED_PROTOCOL_VERSION: 'incorrect protocol version',
    paho.mqtt.client.CONNACK_REFUSED_IDENTIFIER_REJECTED: 'invalid client identifier',
    paho.mqtt.client.CONNACK_REFUSED_SERVER_UNAVAILABLE: 'server unavailable',
    paho.mqtt.client.CONNACK_REFUSED_BAD_USERNAME_PASSWORD: 'bad username or password',
    paho.mqtt.client.CONNACK_REFUSED_NOT_AUTHORIZED: 'not authorised'
}


def mqtt_on_connect(client, userdata, flags, rc):
    logging.info('Connected to MQTT broker with code %s', rc)

    if rc != paho.mqtt.client.CONNACK_ACCEPTED:
        logging.error('Connection refused from reason: %s', mqtt_connect_rc_lut.get(rc, 'unknown code'))

    if rc == paho.mqtt.client.CONNACK_ACCEPTED:
        pass


def mqtt_on_disconnect(client, userdata, rc):
    logging.info('Disconnect from MQTT broker with code %s', rc)


def mqtt_on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    logging.debug('Message %s %s', message.topic, message.payload)
