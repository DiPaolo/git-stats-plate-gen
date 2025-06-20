import datetime
import sys

import click
from PySide6.QtWidgets import QApplication

from git_stats_plate_gen.cli.exit_codes import ExitCode
from git_stats_plate_gen.config import config
from git_stats_plate_gen.core import cache, utils
from git_stats_plate_gen.core.common import get_output_image_filename
from git_stats_plate_gen.core.data import collect_data
from git_stats_plate_gen.gui.preview_widget import PreviewWidget


@click.command()
@click.option('-v', '--version', is_flag=True, default=False,
              help='Print version')
@click.option('-t', '--token', metavar='<token>',
              default=None,
              help="GitHub access token (just google 'Creating a personal access token (classic)'); the following "
                   "permissions are required: read:org, repo")
@click.option('-o', '--output', 'output_base_name', metavar='<filename>',
              default=config.defaults.out_image_base_name, show_default=True,
              help='Output image filename where the graph will be written')
@click.option('--cache/--no-cache', 'use_cache',
              is_flag=True, default=config.defaults.use_cache, show_default=True,
              help='Use cached data to plot graphics')
@click.option('-mp', '--min-percent',
              type=float, default=config.defaults.min_percent,
              help='Lower boundary (%) that language must have to be shown')
def cli(version: bool, token: str, output_base_name: str, use_cache: bool, min_percent: float):
    # print banner
    click.echo(f'{config.application_name} {config.app_version.as_str(4)}\n')

    if version:
        sys.exit(ExitCode.OK.value)

    stats = None
    gen_datetime_utc = None

    if use_cache:
        gen_datetime_utc, stats = cache.load_stats()
        if stats is None:
            click.echo("WARNING: failed to load cache. Will try to collect data from remote...")
        else:
            local_datetime = utils.convert_datetime_utc_to_local(gen_datetime_utc)
            gen_datetime_str = local_datetime.strftime('%Y-%m-%d, %H:%M:%S')
            click.echo(f'Using cache from {gen_datetime_str}')

    if stats is None:
        if token is None:
            token = click.prompt('Token', hide_input=True, default=None)
            if token is None:
                click.echo(
                    "ERROR: token is not specified. Please specify it using '-t'/'--token' command line argument "
                    "or during being asked for in command line prompt", err=True)
                sys.exit(ExitCode.INVALID_CMDLINE_TOKEN.value)

        stats = collect_data(token)
        if stats is not None:
            gen_datetime_utc = datetime.datetime.utcnow()
            cache.save_stats(gen_datetime_utc, stats)

    if stats is None or gen_datetime_utc is None:
        sys.exit(ExitCode.FAILED_COLLECT_STATS.value)

    output_image_name = get_output_image_filename(gen_datetime_utc, output_base_name)

    # we must create GUI application to be able to create a window
    QApplication(sys.argv)
    preview = PreviewWidget()

    preview.set_data(gen_datetime_utc, stats, min_percent)
    preview.save_image(output_image_name)

    sys.exit(ExitCode.OK.value)
