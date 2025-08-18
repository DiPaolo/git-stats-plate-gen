import dataclasses
from typing import Dict


@dataclasses.dataclass
class RepoInfo:
    _name: str
    _visibility: str

    def __init__(self, repo_info: Dict):
        self._name = repo_info['name']
        self._visibility = 'private' if repo_info['private'] is True else 'public'
