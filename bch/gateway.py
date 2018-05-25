#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import time


@click.group(help="Gateway")
@click.pass_context
def gw(ctx):
    pass


@gw.command("list")
@click.pass_context
def gw_list(ctx):

    def on_message(client, topic, payload):
        print(topic.split('/')[1], payload)

    mqttc = ctx.obj['mqttc']
    mqttc.on_message = on_message
    mqttc.subscribe("gateway/+/info")
    mqttc.publish("gateway/all/info/get")

    time.sleep(1)
