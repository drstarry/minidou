# coding: utf-8

import click
import os
from .cli import pass_context

from minidou.server.server import run_server


@click.command('run', short_help='run minidou')
@click.option('-m', '--mode',
              default='debug',
              type=click.Choice(['debug', 'prod']),
              help='running mode, either debug or prod')
@click.option('-p', '--port',
              default=8080,
              type=int,
              help='port minidou')
@pass_context
def cli(ctx, mode, port):
	run_server(port=port)
