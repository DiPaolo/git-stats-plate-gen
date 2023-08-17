import datetime
import pprint
import sys
from typing import Dict

import click

from gh_repo_stats import config
from gh_repo_stats.cli.exit_codes import ExitCode
from gh_repo_stats.core import cache
from gh_repo_stats.core.common import DataType, get_data_type_name
from gh_repo_stats.core.data import collect_data
from gh_repo_stats.core.graph import plot_graph


@click.command()
@click.option('-u', '--user', metavar='<name>', default=None,
              help='GitHub username')
@click.option('-t', '--token', metavar='<token>', default=None,
              help="GitHub token (here is the link to GitHub documentation page http://shorturl.at/psGQS, or "
                   "just google 'GitHub Creating a personal access token'); you need only to grant access to"
                   "Repository permissions: Read access to code, commit statuses, and metadata")
@click.option('-o', '--output', 'output_base_name', metavar='<filename>', default='github_lang_stats',
              show_default=True, help='Output image filename where the graph will be written')
@click.option('--cache', 'use_cache', is_flag=True, default=False, show_default=True,
              help='Use cached data to plot graphics')
@click.option('-mp', '--min-percent', type=float, default=1.0,
              help='Lower boundary (in %) that language must have to be shown')
def cli(user: str, token: str, output_base_name: str, use_cache: bool, min_percent: float):
    if not cache and user is None:
        click.echo("ERROR: user is not specified. Please specify it using '-u'/'--user' command line argument")
        sys.exit(ExitCode.INVALID_CMDLINE_USER.value)

    stats = None

    if use_cache:
        stats = cache.load_stats()

    if stats is None:
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

    _plot_graph(stats, DataType.BYTES, min_percent, output_base_name)
    _plot_graph(stats, DataType.LINES, min_percent, output_base_name)

    sys.exit(ExitCode.OK.value)


def _plot_graph(stats: Dict, data_type: DataType, min_percent: float, output_base_name: str):
    param_name = get_data_type_name(data_type)

    lang_stats_bytes = {k: v[param_name] if param_name in v else 0 for k, v in stats.items()}
    sorted_lang_stats = sorted(lang_stats_bytes.items(), key=lambda x: x[1], reverse=True)
    plot_graph(sorted_lang_stats, data_type, min_percent,
               f"{output_base_name}_{param_name}_{datetime.datetime.now().strftime('%Y-%m-%d')}.png")

    total_code = sum(code_bytes for lang, code_bytes in sorted_lang_stats)

    if config.DEBUG:
        pprint.pprint(sorted_lang_stats)

    click.echo(f'Total {param_name}: {total_code}')
    for lang, code in sorted_lang_stats:
        click.echo(f'  {lang} - {code} ({code * 100.0 / total_code :4.2f}%)')
