from cachetools import TTLCache

# Create a cache with a default TTL of 5 minutes and maxsize 1024
# The TTL can be overridden per call if needed, but we keep simple.
ttl_cache = TTLCache(maxsize=1024, ttl=300)

def get(key):
    return ttl_cache.get(key)

def set(key, value, ttl=None):
    # ttl parameter is ignored for simplicity; use global ttl.
    ttl_cache[key] = value

def delete(key):
    ttl_cache.pop(key, None)

def clear():
    ttl_cache.clear()