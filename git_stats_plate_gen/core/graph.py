import datetime
import os.path
from typing import Dict

import click

from git_stats_plate_gen.config import config
from git_stats_plate_gen.core.common import DataType, get_data_type_name


def map_data_type_to_text(data_type: DataType) -> str:
    if data_type == DataType.BYTES:
        return 'bytes'
    elif data_type == DataType.LINES:
        return 'lines of code'

    return map_data_type_to_text(data_type)


def plot_graph_to_file(stats: Dict, data_type: DataType = DataType.LINES, min_percent: float = 1.0,
                       output_dir: str = '.', output_base_name: str = 'github_langs_stats',
                       width: int = config.defaults.image_width, height: int = config.defaults.image_height):
    param_name = get_data_type_name(data_type)
    output_filename = f"{output_base_name}_{param_name}_{datetime.datetime.now().strftime('%Y-%m-%d')}.png"
    output_full_abs_filename = os.path.abspath(os.path.join(output_dir, output_filename))
    # fig, total_code = _plot_graph_internal(stats, data_type, min_percent)

    # fig.write_image(output_full_abs_filename, width=width, height=height)

    click.echo()
    click.echo(f'Statistics for {get_data_type_name(data_type)} has been saved to {output_full_abs_filename}')
    # click.echo(f'Total {param_name}: {total_code}')

    return output_full_abs_filename
