import pprint
import tempfile
from typing import Dict

import click

from gh_repo_stats.core.github import clone_repo, calc_lines_local_repo
from gh_repo_stats.core.graph import plot_graph


@click.command()
@click.option('-t', '--token', prompt=True, hide_input=True, metavar='<token>',
              help="GitHub token (here is the link to GitHub documentation page http://shorturl.at/psGQS, or "
                   "just google 'GitHub Creating a personal access token'); you need only to grant access to"
                   "Repository permissions: Read access to code, commit statuses, and metadata")
@click.option('-o', '--output', 'output_base_name', metavar='<filename>', default='github_lang_stats',
              show_default=True, help='Output image filename where the graph will be written')
@click.option('--cache', is_flag=True, default=False, show_default=True,
              help='Use cached data to plot graphics')
def cli(token: str, output_base_name: str, cache: bool):
    if token.startswith('github'):
        from gh_repo_stats.core.github import get_repo_langs, get_repos
    else:
        from gh_repo_stats.core.gitlab import get_repo_langs, get_repos

    repos = get_repos(token)
    print(f'Total {len(repos)} repos')

    if len(repos) == 0:
        return

    lang_stats = dict()
    for repo in repos:
        permissions = repo['permissions']
        if permissions['admin'] is True:
            permission_str = 'admin'
        elif permissions['maintain'] is True:
            permission_str = 'admin'
        else:
            permission_str = 'other'

        is_fork = repo['fork']
        fork_info_str = 'fork' if is_fork else 'own'

        print(f"{repo['name']} ({'private' if repo['private'] else 'public'}, {permission_str}, {fork_info_str}): "
              f"{repo['language']}")

        if is_fork:
            continue

        if repo['language'] is None:
            pass

        # main
        cur_repo_lang_stats = _calc_main(token, repo)
        bytes_mapping = {
            'C': 'C/C++',
            'C++': 'C/C++',
        }
        for lang, code_bytes in cur_repo_lang_stats.items():
            if lang in bytes_mapping:
                lang = bytes_mapping[lang]

            if lang is None:
                continue

            if lang not in lang_stats:
                lang_stats[lang] = dict()

            if 'bytes' not in lang_stats[lang]:
                lang_stats[lang]['bytes'] = 0

            lang_stats[lang]['bytes'] += code_bytes

        # lines
        lines_stats = _calc_repo_lines(repo['name'])
        lines_mapping = {
            'Bourne Shell': 'Shell',
            'Bourne Again Shell': 'Shell',
            'DOS Batch': 'Batchfile',
            'make': 'Makefile',
            'Vuejs Component': 'Vue',
            'C': 'C/C++',
            'C++': 'C/C++',
            'C/C++ Header': 'C/C++',
            'JSON': None
        }
        for lang, lines in lines_stats.items():
            if lang in lines_mapping:
                lang = lines_mapping[lang]

            if lang is None:
                continue

            if lang not in lang_stats:
                lang_stats[lang] = dict()

            if 'lines' not in lang_stats[lang]:
                lang_stats[lang]['lines'] = 0

            lang_stats[lang]['lines'] += lines

    lang_stats_bytes = {k: v['bytes'] if 'bytes' in v else 0 for k, v in lang_stats.items()}
    sorted_lang_stats_bytes = sorted(lang_stats_bytes.items(), key=lambda x: x[1], reverse=True)
    plot_graph(sorted_lang_stats_bytes, f'{output_base_name}_bytes.png')

    total_code_bytes = sum(code_bytes for lang, code_bytes in sorted_lang_stats_bytes)
    pprint.pprint(sorted_lang_stats_bytes)

    print(f'Total bytes: {total_code_bytes}')
    for lang, code_bytes in sorted_lang_stats_bytes:
        print(f'  {lang} - {code_bytes} ({code_bytes * 100.0 / total_code_bytes :4.2f}%)')

    lang_stats_lines = {k: v['lines'] if 'lines' in v else 0 for k, v in lang_stats.items()}
    sorted_lang_stats_lines = sorted(lang_stats_lines.items(), key=lambda x: x[1], reverse=True)
    plot_graph(sorted_lang_stats_lines, f'{output_base_name}_lines.png')

    total_code_lines = sum(code_lines for lang, code_lines in sorted_lang_stats_lines)
    pprint.pprint(sorted_lang_stats_lines)

    print(f'Total lines: {total_code_lines}')
    for lang, code_lines in sorted_lang_stats_lines:
        print(f'  {lang} - {code_lines} ({code_lines * 100.0 / total_code_lines :4.2f}%)')


def _calc_main(token: str, repo: Dict):
    if token.startswith('github'):
        from gh_repo_stats.core.github import get_repo_langs, get_repos
    else:
        from gh_repo_stats.core.gitlab import get_repo_langs, get_repos

    repo_langs = get_repo_langs(token, repo['name'])
    pprint.pprint(repo_langs)

    lang_stats = dict()
    for lang, code_bytes in repo_langs.items():
        if lang in lang_stats:
            lang_stats[lang] += int(code_bytes)
        else:
            lang_stats[lang] = code_bytes

    return lang_stats


def _calc_repo_lines(repo_name: str) -> Dict:
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_dir = clone_repo(repo_name, tmp_dir)
        if repo_dir:
            return calc_lines_local_repo(repo_dir)

    return dict()
