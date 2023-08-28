import datetime
import sys

import click

from git_stats_plate_gen.cli.exit_codes import ExitCode
from git_stats_plate_gen.config import config
from git_stats_plate_gen.core import cache, utils
from git_stats_plate_gen.core.common import DataType
from git_stats_plate_gen.core.data import collect_data
from git_stats_plate_gen.core.graph import plot_graph_to_file


@click.command()
@click.option('-v', '--version', is_flag=True, default=False,
              help='Print version')
@click.option('-u', '--user', metavar='<name>',
              default=None,
              help='GitHub username')
@click.option('-t', '--token', metavar='<token>',
              default=None,
              help="GitHub token (just google 'GitHub Creating a personal access token'); you need only to grant "
                   "access to Repository permissions: Read access to code, commit statuses, and metadata")
@click.option('-o', '--output', 'output_base_name', metavar='<filename>',
              default=config.defaults.out_image_base_name, show_default=True,
              help='Output image filename where the graph will be written')
@click.option('--cache/--no-cache', 'use_cache',
              is_flag=True, default=config.defaults.use_cache, show_default=True,
              help='Use cached data to plot graphics')
@click.option('-mp', '--min-percent',
              type=float, default=config.defaults.min_percent,
              help='Lower boundary (%) that language must have to be shown')
def cli(version: bool, user: str, token: str, output_base_name: str, use_cache: bool, min_percent: float):
    # print banner
    click.echo(f'{config.application_name} {config.app_version.as_str(4)}\n')

    if version:
        sys.exit(ExitCode.OK.value)

    if not use_cache and user is None:
        click.echo("ERROR: user is not specified. Please specify it using '-u'/'--user' command line argument",
                   err=True)
        sys.exit(ExitCode.INVALID_CMDLINE_USER.value)

    stats = None

    if use_cache:
        gen_datetime_utc, stats = cache.load_stats()
        if stats is None:
            click.echo("WARNING: failed to load cache. Will try to collect data from remote...")
        else:
            local_datetime = utils.convert_datetime_utc_to_local(gen_datetime_utc)
            gen_datetime_str = local_datetime.strftime('%Y-%m-%d, %H:%M:%S')
            click.echo(f'Using cache from {gen_datetime_str}')

    if stats is None:
        if user is None:
            click.echo("ERROR: user is not specified. Please specify it using '-u'/'--user' command line "
                       "argument", err=True)
            sys.exit(ExitCode.INVALID_CMDLINE_USER.value)

        if token is None:
            token = click.prompt('Token', hide_input=True, default=None)
            if token is None:
                click.echo(
                    "ERROR: token is not specified. Please specify it using '-t'/'--token' command line argument "
                    "or during being asked for in command line prompt", err=True)
                sys.exit(ExitCode.INVALID_CMDLINE_TOKEN.value)

        stats = collect_data(user, token)
        if stats is not None:
            cache.save_stats(datetime.datetime.utcnow(), stats)

    if stats is None:
        sys.exit(ExitCode.FAILED_COLLECT_STATS.value)

    plot_graph_to_file(stats, DataType.BYTES, min_percent, output_base_name=output_base_name)
    plot_graph_to_file(stats, DataType.LINES, min_percent, output_base_name=output_base_name)

    sys.exit(ExitCode.OK.value)
