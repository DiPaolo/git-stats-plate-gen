import datetime
import pickle
from typing import Dict, Optional

_CACHE_FILENAME = '.stats_cache.dat'
_CUR_VERSION = 1


def load_stats() -> (Optional[datetime.datetime], Optional[Dict]):
    """

    :return: datetime (UTC) when generated + stats as a second parameter
    """
    try:
        with open(_CACHE_FILENAME, 'rb') as f:
            data = pickle.load(f)
            if 'version' not in data or 'datetime_utc' not in data or 'stats' not in data:
                return None, None

            try:
                version = int(data['version'])
            except TypeError:
                return None, None

            if version != _CUR_VERSION:
                return None, None

            try:
                gen_datetime_utc = datetime.datetime.fromisoformat(data['datetime_utc'])
            except ValueError:
                return None, None

            if not isinstance(data['stats'], Dict):
                return None, None

            return gen_datetime_utc, data['stats']
    except FileNotFoundError:
        return None, None


def save_stats(gen_datetime_utc: datetime.datetime, stats: Dict):
    with open(_CACHE_FILENAME, 'wb') as f:
        pickle.dump({'version': _CUR_VERSION, 'datetime_utc': gen_datetime_utc.isoformat(), 'stats': stats}, f)
