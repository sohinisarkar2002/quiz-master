import redis

cache = redis.Redis(host="localhost", port=6379, db=0)

def cache_set(key, value, expiry=3600):
    """Set a key-value pair in cache with an expiry time (default 1 hour)."""
    cache.setex(key, expiry, value)

def cache_get(key):
    """Retrieve a value from cache."""
    return cache.get(key)

def cache_delete(key):
    """Delete a key from cache."""
    cache.delete(key)
