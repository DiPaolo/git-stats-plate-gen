from typing import List, Tuple

import plotly.graph_objects as go

from gh_repo_stats.core.common import DataType, get_data_type_name


def map_data_type_to_text(data_type: DataType) -> str:
    if data_type == DataType.BYTES:
        return 'bytes'
    elif data_type == DataType.LINES:
        return 'lines of code'

    return map_data_type_to_text(data_type)


def plot_graph(lang_stats: List[Tuple[str, int]], data_type: DataType, min_percent: float, output_filename: str):
    sorted_lang_stats = sorted(lang_stats, key=lambda x: x[1])
    total_code_bytes = sum(code_bytes for lang, code_bytes in sorted_lang_stats)
    # print(total_code_bytes)

    min_abs_value = total_code_bytes * min_percent / 100.0
    sorted_lang_stats = list(filter(lambda x: x if x[1] >= min_abs_value else None, sorted_lang_stats))

    fig = go.Figure(
        go.Bar(
            # x=[code_bytes * 100.0 / total_code_bytes for lang, code_bytes in sorted_lang_stats],
            x=[code_bytes for lang, code_bytes in sorted_lang_stats],
            y=[lang for lang, code_bytes in sorted_lang_stats],
            marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ),
            orientation='h',
            texttemplate='%{x}',
        ),
        layout_title_text=f'Most used languages ({map_data_type_to_text(data_type)})',
        layout_title_font_size=36
    )

    y_s = [round(code_bytes * 100.0 / total_code_bytes, 1) for lang, code_bytes in sorted_lang_stats]
    x = [lang for lang, code_bytes in sorted_lang_stats]

    annotations = []

    # Adding labels
    for yd, xd in zip(y_s, x):
        annotations.append(dict(xref='x1', yref='y1',
                                # x=-200, y=-100,
                                y=xd, x=min(500, 500),
                                text=f'{yd} %',
                                font=dict(family='Arial', size=12,
                                          color='rgb(69, 75, 27)'),
                                showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper',
                            x=0, y=-0.109,
                            text='Generated by gh-repo-stats (https://github.com/DiPaolo/gh-repo-stats)',
                            font=dict(size=16, color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)

    fig.write_image(output_filename, width=1280, height=720)
    print(f'\n'
          f'Statistics for {get_data_type_name(data_type)} has been written to {output_filename}')
