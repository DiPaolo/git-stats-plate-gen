import pprint
import sys
from typing import Dict

import click

from gh_repo_stats.core import cache
from gh_repo_stats.core.data import collect_data
from gh_repo_stats.core.graph import plot_graph


@click.command()
@click.option('-t', '--token',
              # prompt=True,
              # hide_input=True,
              metavar='<token>',
              default=None,
              help="GitHub token (here is the link to GitHub documentation page http://shorturl.at/psGQS, or "
                   "just google 'GitHub Creating a personal access token'); you need only to grant access to"
                   "Repository permissions: Read access to code, commit statuses, and metadata")
@click.option('-o', '--output', 'output_base_name', metavar='<filename>', default='github_lang_stats',
              show_default=True, help='Output image filename where the graph will be written')
@click.option('--cache', 'use_cache', is_flag=True, default=False, show_default=True,
              help='Use cached data to plot graphics')
def cli(token: str, output_base_name: str, use_cache: bool):
    stats = None

    if use_cache:
        stats = cache.load_stats()

    if stats is None:
        if token is None:
            token = click.prompt('Token', hide_input=True, default=None)
            if token is None:
                click.echo('ERROR: Token is not specified. Please specify it using command line argument or via '
                           'command line prompt')
                sys.exit(1)

        stats = collect_data(token)
        if stats is not None:
            cache.dump_stats(stats)

    if stats is None:
        sys.exit(2)

    _plot_graph(stats, 'bytes', output_base_name)
    _plot_graph(stats, 'lines', output_base_name)

    sys.exit(0)


def _plot_graph(stats: Dict, param_name: str, output_base_name: str):
    lang_stats_bytes = {k: v[param_name] if param_name in v else 0 for k, v in stats.items()}
    sorted_lang_stats = sorted(lang_stats_bytes.items(), key=lambda x: x[1], reverse=True)
    plot_graph(sorted_lang_stats, f'{output_base_name}_{param_name}.png')

    total_code = sum(code_bytes for lang, code_bytes in sorted_lang_stats)
    pprint.pprint(sorted_lang_stats)

    print(f'Total {param_name}: {total_code}')
    for lang, code in sorted_lang_stats:
        print(f'  {lang} - {code} ({code * 100.0 / total_code :4.2f}%)')
