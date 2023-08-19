import sys

import click

from gh_repo_stats import config
from gh_repo_stats.cli.exit_codes import ExitCode
from gh_repo_stats.core import cache
from gh_repo_stats.core.common import DataType
from gh_repo_stats.core.data import collect_data
from gh_repo_stats.core.graph import plot_graph_to_file


@click.command()
@click.option('-u', '--user', metavar='<name>',
              default=None,
              help='GitHub username')
@click.option('-t', '--token', metavar='<token>',
              default=None,
              help="GitHub token (here is the link to GitHub documentation page http://shorturl.at/psGQS, or "
                   "just google 'GitHub Creating a personal access token'); you need only to grant access to"
                   "Repository permissions: Read access to code, commit statuses, and metadata")
@click.option('-o', '--output', 'output_base_name', metavar='<filename>',
              default=config.DEFAULT_OUT_IMAGE_BASE_NAME, show_default=True,
              help='Output image filename where the graph will be written')
@click.option('--cache/--no-cache', 'use_cache',
              is_flag=True, default=config.DEFAULT_USE_CACHE, show_default=True,
              help='Use cached data to plot graphics')
@click.option('-mp', '--min-percent',
              type=float, default=config.DEFAULT_MIN_PERCENT,
              help='Lower boundary (%) that language must have to be shown')
def cli(user: str, token: str, output_base_name: str, use_cache: bool, min_percent: float):
    if not use_cache and user is None:
        click.echo("ERROR: user is not specified. Please specify it using '-u'/'--user' command line argument")
        sys.exit(ExitCode.INVALID_CMDLINE_USER.value)

    stats = None

    if use_cache:
        stats = cache.load_stats()
        if stats is None:
            click.echo("WARNING: failed to load cache. Will try to gather data from remote...")

    if stats is None:
        if user is None:
            click.echo("ERROR: user is not specified. Please specify it using '-u'/'--user' command line argument")
            sys.exit(ExitCode.INVALID_CMDLINE_USER.value)

        if token is None:
            token = click.prompt('Token', hide_input=True, default=None)
            if token is None:
                click.echo(
                    "ERROR: token is not specified. Please specify it using '-t'/'--token' command line argument "
                    "or during being asked for in command line prompt")
                sys.exit(ExitCode.INVALID_CMDLINE_TOKEN.value)

        stats = collect_data(user, token)
        if stats is not None:
            cache.dump_stats(stats)

    if stats is None:
        sys.exit(ExitCode.FAILED_COLLECT_STATS.value)

    plot_graph_to_file(stats, DataType.BYTES, min_percent, output_base_name=output_base_name)
    plot_graph_to_file(stats, DataType.LINES, min_percent, output_base_name=output_base_name)

    sys.exit(ExitCode.OK.value)
