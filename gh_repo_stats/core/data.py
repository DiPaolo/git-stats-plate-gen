import pprint
import tempfile
from typing import Dict

from gh_repo_stats import config
from gh_repo_stats.core.github import clone_repo, calc_lines_local_repo


def collect_data(user_name: str, token: str):
    if token.startswith('github'):
        from gh_repo_stats.core.github import get_repo_langs, get_repos
    else:
        from gh_repo_stats.core.gitlab import get_repo_langs, get_repos

    repos = get_repos(token)

    if config.DEBUG:
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

        if config.DEBUG:
            print(f"{repo['name']} ({'private' if repo['private'] else 'public'}, {permission_str}, {fork_info_str}): "
                  f"{repo['language']}")

        if is_fork:
            continue

        if repo['language'] is None:
            pass

        # main
        cur_repo_lang_stats = _calc_main(user_name, token, repo)
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
        lines_stats = _calc_repo_lines(user_name, repo['name'])
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

    return lang_stats


def _calc_main(user_name: str, token: str, repo: Dict):
    if token.startswith('github'):
        from gh_repo_stats.core.github import get_repo_langs
    else:
        from gh_repo_stats.core.gitlab import get_repo_langs

    repo_langs = get_repo_langs(user_name, token, repo['name'])
    if config.DEBUG:
        pprint.pprint(repo_langs)

    lang_stats = dict()
    for lang, code_bytes in repo_langs.items():
        if lang in lang_stats:
            lang_stats[lang] += int(code_bytes)
        else:
            lang_stats[lang] = code_bytes

    return lang_stats


def _calc_repo_lines(user_name: str, repo_name: str) -> Dict:
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_dir = clone_repo(user_name, repo_name, tmp_dir)
        if repo_dir:
            return calc_lines_local_repo(repo_dir)

    return dict()
