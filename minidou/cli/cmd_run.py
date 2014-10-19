# coding: utf-8

import click
from .cli import pass_context

from minidou.server import run_server


@click.command('run', short_help='run minidou')
@click.option('-p', '--port',
              default=8080,
              type=int,
              help='port minidou')
@pass_context
def cli(ctx, mode, port):
    run_server(port=port)
