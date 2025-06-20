import json
import os.path
import subprocess
from typing import List, Dict

import click
import requests

from git_stats_plate_gen.config import config


def get_repos(token: str) -> List[Dict]:
    out = list()

    cur_page = 0
    while True:
        cur_page_repos = _get_repos_page(token, cur_page)
        out += cur_page_repos
        if len(cur_page_repos) < 100:
            break

        cur_page += 1

    return out


def _get_repos_page(token: str, page: int) -> List[Dict]:
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    ret = requests.get(f'https://api.github.com/user/repos?per_page=100&page={page + 1}', headers=headers)
    if not ret.ok:
        click.echo(f"Failed to get repos from GitHub: {ret.reason}", err=True)
        return list()

    data = json.loads(ret.text)
    return data


def get_repo_langs(token: str, repo: Dict) -> List[Dict]:
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    ret = requests.get(f"{repo['url']}/languages", headers=headers)
    if not ret.ok:
        click.echo(f"Failed to get languages for repo {repo['name']} from GitHub: {ret.reason}", err=True)
        return list()

    data = json.loads(ret.text)
    return data


def clone_repo(repo: Dict, working_dir: str):
    cmdline = ['git', 'clone', repo['ssh_url']]
    result = subprocess.run(cmdline, cwd=working_dir, capture_output=True, universal_newlines=True, timeout=5 * 60)

    if config.is_debug:
        print(f"=== ret code = {result.returncode} ===\n"
              f"   stdout: \n{result.stdout}\n\n"
              f"   stderr: \n{result.stderr}\n"
              f"=============================")

    if result.returncode != 0:
        return None

    return os.path.join(working_dir, repo['name'])


def calc_lines_local_repo(repo_dir: str) -> Dict:
    cmdline = ['cloc', '.', '--json']
    result = subprocess.run(cmdline, cwd=repo_dir, capture_output=True, universal_newlines=True, timeout=5 * 60)

    if config.is_debug:
        print(f"=== ret code = {result.returncode} ===\n"
              f"   stdout: \n{result.stdout}\n\n"
              f"   stderr: \n{result.stderr}\n"
              f"=============================")

    data = json.loads(result.stdout)

    lines_by_lang = dict()
    for key, value in data.items():
        if key in ['header', 'SUM']:
            continue

        lines_by_lang[key] = value['blank'] + value['comment'] + value['code']

    return lines_by_lang
