import json
from typing import List, Dict

import click
import requests


def get_my_user_id(token: str) -> int:
    headers = {
        # 'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        # 'X-GitHub-Api-Version': '2022-11-28'
    }
    ret = requests.get('https://gitlab.com/api/v4/user', headers=headers)
    if not ret.ok:
        click.echo(f"Failed to get user ID from GitLab: {ret.reason}", err=True)
        return -1

    data = json.loads(ret.text)
    if 'id' not in data:
        click.echo(f"Failed to get user ID from GitLab: failed to find 'ID' field in returned data", err=True)
        return -1

    return data['id']


def get_groups(token: str, group_id: int) -> List[object]:
    if group_id <= 0:
        return list()

    headers = {
        # 'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        # 'X-GitHub-Api-Version': '2022-11-28'
    }
    ret = requests.get(f'https://gitlab.com/api/v4/groups/{group_id}/projects', headers=headers)
    if not ret.ok:
        click.echo(f"Failed to get repos from GitLab: {ret.reason}", err=True)
        return list()

    data = json.loads(ret.text)
    return data


def get_namespaces(token: str) -> List[object]:
    user_id = get_my_user_id(token)
    if user_id <= 0:
        return list()

    headers = {
        # 'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        # 'X-GitHub-Api-Version': '2022-11-28'
    }
    ret = requests.get(f'https://gitlab.com/api/v4/namespaces', headers=headers)
    if not ret.ok:
        click.echo(f"Failed to get repos from GitLab: {ret.reason}", err=True)
        return list()

    data = json.loads(ret.text)

    for group in data:
        get_groups(token, group['id'])

    return data


def get_repos(token: str) -> List[object]:
    get_namespaces(token)

    user_id = get_my_user_id(token)
    if user_id <= 0:
        return list()

    headers = {
        # 'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        # 'X-GitHub-Api-Version': '2022-11-28'
    }
    ret = requests.get(f'https://gitlab.com/api/v4/users/{user_id}/projects?per_page=100', headers=headers)
    if not ret.ok:
        click.echo(f"Failed to get repos from GitLab: {ret.reason}", err=True)
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
