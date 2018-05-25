#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click


def print_table(labels, rows):
    if not labels and not rows:
        return

    max_lengths = [0] * (len(rows[0]) if rows else len(labels))
    for i, label in enumerate(labels):
        max_lengths[i] = len(label)

    for row in rows:
        for i, v in enumerate(row):
            if len(v) > max_lengths[i]:
                max_lengths[i] = len(v)

    row_format = "{:<" + "}  {:<".join(map(str, max_lengths)) + "}"

    if labels:
        click.echo(row_format.format(*labels))
        click.echo("=" * (sum(max_lengths) + len(labels) * 2))

    for row in rows:
        click.echo(row_format.format(*row))
