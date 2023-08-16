import json
import os.path
import subprocess
import tempfile
from typing import List, Dict

import click
import requests


def get_repos(token: str) -> List[Dict]:
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    ret = requests.get('https://api.github.com/user/repos?per_page=100', headers=headers)
    if not ret.ok:
        click.echo(f"Failed to get repos from GitHub: {ret.reason}", err=True)
        return list()

    data = json.loads(ret.text)
    return data


def get_repo_langs(token: str, repo_name: str) -> List[Dict]:
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    ret = requests.get(f'https://api.github.com/repos/dipaolo/{repo_name}/languages', headers=headers)
    if not ret.ok:
        click.echo(f"Failed to get languages for repo {repo_name} from GitHub: {ret.reason}", err=True)
        return list()

    data = json.loads(ret.text)
    return data


def clone_repo(repo_name: str, working_dir: str):
    cmdline = ['git', 'clone', f'git@github.com:DiPaolo/{repo_name}.git']
    result = subprocess.run(cmdline, cwd=working_dir, capture_output=True, universal_newlines=True, timeout=5 * 60)

    # print(f"=== ret code = {result.returncode} ===\n"
    #       f"   stdout: \n{result.stdout}\n\n"
    #       f"   stderr: \n{result.stderr}\n"
    #       f"=============================")

    if result.returncode != 0:
        return  None

    return os.path.join(working_dir, repo_name)

def calc_lines_local_repo(repo_dir: str) -> Dict:
    cmdline = ['cloc', '.', '--json']
    result = subprocess.run(cmdline, cwd=repo_dir, capture_output=True, universal_newlines=True, timeout=5 * 60)

    # print(f"=== ret code = {result.returncode} ===\n"
    #       f"   stdout: \n{result.stdout}\n\n"
    #       f"   stderr: \n{result.stderr}\n"
    #       f"=============================")

    data = json.loads(result.stdout)

    lines_by_lang = dict()
    for key, value in data.items():
        if key in ['header', 'SUM']:
            continue

        lines_by_lang[key] = value['blank'] + value['comment'] + value['code']

    return lines_by_lang