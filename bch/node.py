#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from bch.tools import print_table


def get_nodes(ctx):
    gateway = ctx.obj['gateway']

    response = ctx.obj['mqttc'].command(["gateway", gateway, "nodes/get"], None, ["gateway", gateway, "nodes"])

    return response['payload'] if response else []


def find_node(id_or_alias, nodes):
    for node in nodes:
        if node['id'] == id_or_alias or node.get('alias', '') == id_or_alias:
            return node


@click.group(help="")
@click.pass_context
def node(ctx):
    pass


@node.command("list")
@click.pass_context
def node_list(ctx):
    nodes = get_nodes(ctx)

    rows = [[node['id'], node.get('alias', '')] for node in nodes]

    print_table(['id', 'alias'], rows)


@node.command("rename")
@click.argument('id_or_alias')
@click.argument('new_alias')
@click.pass_context
def node_rename(ctx, id_or_alias, new_alias):

    node = find_node(id_or_alias, get_nodes(ctx))

    if not node:
        click.echo("Unknown node")
        return

    if new_alias == '':
        new_alias = None

    if node.get('alias', None) == new_alias:
        click.echo("Alias is already set")
        return

    gateway = ctx.obj['gateway']
    response = ctx.obj['mqttc'].command(["gateway", gateway, "alias/set"], {"id": node['id'], 'alias': new_alias}, ["gateway", gateway, "alias/set/ok"], timeout=5)

    if not response:
        click.echo("Error, empty response")
        return

    if node['id'] == response['payload']['id'] and response['payload']['alias'] == new_alias:
        click.echo("OK")
    else:
        click.echo("Error, not match")


@node.command("remove")
@click.argument('id_or_alias')
@click.pass_context
def node_remove(ctx, id_or_alias):
    node = find_node(id_or_alias, get_nodes(ctx))

    if not node:
        click.echo("Unknown node")
        return

    gateway = ctx.obj['gateway']
    response = ctx.obj['mqttc'].command(["gateway", gateway, "nodes/remove"], node['id'], ["gateway", gateway, "detach"], timeout=5)

    if not response:
        click.echo("Error, empty response")
        return

    if response['payload'] == node['id']:
        click.echo("OK")
    else:
        click.echo("Error")


@node.command("add")
@click.argument('id')
@click.pass_context
def node_remove(ctx, id):
    node = find_node(id, get_nodes(ctx))

    if node:
        click.echo("Ignore node is in node list")
        return

    gateway = ctx.obj['gateway']
    response = ctx.obj['mqttc'].command(["gateway", gateway, "nodes/add"], id, ["gateway", gateway, "attach"], timeout=5)

    if not response:
        click.echo("Error, empty response")
        return

    if response['payload'] == id:
        click.echo("OK")
    else:
        click.echo("Error")
