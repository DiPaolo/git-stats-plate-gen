import pickle
from typing import Dict, Optional

_CACHE_FILENAME = '.stats_cache.dat'
_CUR_VERSION = 1


def dump_stats(stats: Dict):
    with open(_CACHE_FILENAME, 'wb') as f:
        pickle.dump({'version': _CUR_VERSION, 'stats': stats}, f)


def load_stats() -> Optional[Dict]:
    """

    :return: version of the dict (stats) + stats as a second parameter
    """
    try:
        with open(_CACHE_FILENAME, 'rb') as f:
            data = pickle.load(f)
            if 'version' not in data or 'stats' not in data:
                return None

            try:
                version = int(data['version'])
            except TypeError:
                return None

            if version != _CUR_VERSION:
                return None

            if not isinstance(data['stats'], Dict):
                return None

            return data['stats']
    except:
        return None
