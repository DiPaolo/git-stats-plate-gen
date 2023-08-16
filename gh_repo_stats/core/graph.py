from typing import List, Tuple

import plotly.graph_objects as go


def plot_graph(lang_stats: List[Tuple[str, int]], min_percent: float, output_filename: str):
    sorted_lang_stats = sorted(lang_stats, key=lambda x: x[1])
    total_code_bytes = sum(code_bytes for lang, code_bytes in sorted_lang_stats)
    # print(total_code_bytes)

    min_abs_value = total_code_bytes * min_percent / 100.0
    sorted_lang_stats = list(filter(lambda x: x if x[1] >= min_abs_value else None, sorted_lang_stats))

    fig = go.Figure(go.Bar(
        x=[code_bytes * 100.0 / total_code_bytes for lang, code_bytes in sorted_lang_stats],
        y=[lang for lang, code_bytes in sorted_lang_stats],
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),
        ),
        orientation='h'), layout_title_text='Most used languages',
    )

    annotations = []

    # y_s = np.round(y_saving, decimals=2)
    y_s = [round(code_bytes * 100.0 / total_code_bytes, 1) for lang, code_bytes in sorted_lang_stats]
    # y_nw = np.rint(y_net_worth)
    x = [lang for lang, code_bytes in sorted_lang_stats]

    # Adding labels
    for yd, xd in zip(y_s, x):
        annotations.append(dict(xref='x1', yref='y1',
                                y=xd, x=yd + 3,
                                text=str(yd) + '%',
                                font=dict(family='Arial', size=12,
                                          color='rgb(50, 171, 96)'),
                                showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper',
                            x=-0.2, y=-0.109,
                            # text='OECD "' +
                            #      '(2015), Household savings (indicator), ' +
                            #      'Household net worth (indicator). doi: ' +
                            #      '10.1787/cfc6f499-en (Accessed on 05 June 2015)',
                            font=dict(family='Arial', size=10, color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)

    fig.write_image(output_filename, width=1280, height=720)
    # fig.show()
    print(f'\n'
          f'Statistics has been written to {output_filename}')
