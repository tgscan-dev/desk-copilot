from desk_copilot.utils.kv_store import KVStore
from toolz import memoize


@memoize
def get_kv_store(file_path):
    return KVStore(file_path)
