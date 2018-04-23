#!/usr/bin/env python3

import os
import sys
import logging
import click
import click_log
import simplejson as json
from datetime import datetime
import paho.mqtt.client
from paho.mqtt.client import topic_matches_sub
from bch.mqtt import *

__version__ = '@@VERSION@@'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logger = logging.getLogger()
handler = click_log.ClickHandler()
handler.setFormatter(click_log.ColorFormatter('%(asctime)s %(message)s'))
logger.addHandler(handler)

userdata = {}
mqttc = paho.mqtt.client.Client(userdata=userdata)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--gateway', type=click.STRING, help="Gateway name [default: usb-dongle].", default="usb-dongle")
@click.option('-H', '--mqtt-host', type=click.STRING, default="127.0.0.1", help="MQTT host to connect to [default: 127.0.0.1].")
@click.option('-P', '--mqtt-port', type=click.IntRange(0, 65535), default=1883, help="MQTT port to connect to [default: 1883].")
@click.option('--mqtt-username', type=click.STRING, help="MQTT username.")
@click.option('--mqtt-password', type=click.STRING, help="MQTT password.")
@click.option('--mqtt-cafile', type=click.Path(exists=True), help="MQTT cafile.")
@click.option('--mqtt-certfile', type=click.Path(exists=True), help="MQTT certfile.")
@click.option('--mqtt-keyfile', type=click.Path(exists=True), help="MQTT keyfile.")
@click_log.simple_verbosity_option(logger, default='WARNING')
def main(gateway, mqtt_host, mqtt_port, mqtt_username, mqtt_password, mqtt_cafile, mqtt_certfile, mqtt_keyfile):

    if mqtt_username:
        self.mqttc.username_pw_set(username, password)

    if mqtt_cafile:
        self.mqttc.tls_set(mqtt_cafile, mqtt_certfile, mqtt_keyfile)

    logging.info('MQTT broker host: %s, port: %d, use tls: %s', mqtt_host, mqtt_port, bool(mqtt_cafile))

    mqttc.connect(mqtt_host, mqtt_port, keepalive=10)
    mqttc.on_connect = mqtt_on_connect
    mqttc.on_disconnect = mqtt_on_disconnect
    mqttc.on_message = mqtt_on_message

    userdata['gateway'] = gateway
    # mqttc.reconnect()


@main.command()
@click.option('--start', 'command', flag_value='start')
@click.option('--stop', 'command', flag_value='stop')
@click.pass_context
def pairing(ctx, command):
    if not command:
        click.echo(pairing.get_help(ctx))
        sys.exit(1)

    mqttc.loop_start()
    msg = mqttc.publish('gateway/' + userdata['gateway'] + '/pairing-mode/' + command, None, qos=1)
    msg.wait_for_publish()


@main.command()
@click.argument('topic', type=click.STRING)
@click.argument('payload', type=click.STRING, required=False)
def pub(topic, payload):
    if payload:
        try:
            payload = json.loads(payload, use_decimal=True)
        except json.decoder.JSONDecodeError as e:
            pass
    mqttc.loop_start()
    msg = mqttc.publish(topic, json.dumps(payload, use_decimal=True), qos=1)
    msg.wait_for_publish()


@main.command(help="Subscribe topic.", epilog="TOPIC [default: #]")
@click.argument('topic', type=click.STRING, default="#")
@click.option('-n', '--number', type=click.INT, help="Number of messages.")
def sub(topic, number):
    def on_message(client, userdata, message):
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:22]
        click.echo(dt + ' ' + message.topic + ' ' + message.payload.decode('utf-8'))
        on_message.cnt += 1
        if number and on_message.cnt == number:
            sys.exit(0)

    on_message.cnt = 0
    mqttc.on_message = on_message
    mqttc.subscribe(topic)
    mqttc.loop_forever()


@main.command(help="Show program's version number and exit.")
def version():
    click.echo(__version__)
