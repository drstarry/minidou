# coding: utf-8

import sys
import os
import logging

import click
from click import echo


class Context(object):
    def __init__(self):
        self.verbose = False

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.dirname(__file__))


class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__('minidou.cli.cmd_' +
                             name.encode('ascii', 'replace'),
                             None, None, ['cli'])
        except ImportError as e:
            echo(click.style(str(e), fg='red'))
            return
        return mod.cli


@click.command(cls=ComplexCLI)
@click.option('-v', '--verbose', default=False, is_flag=True, help='Enables verbose mode.')
@pass_context
def cli(ctx, verbose):
    ctx.verbose = verbose
    tracer = logging.getLogger('elasticsearch')
    tracer.setLevel(logging.INFO if verbose else logging.WARNING)
    tracer.addHandler(logging.StreamHandler(sys.stdout))


def main():
    cli()
