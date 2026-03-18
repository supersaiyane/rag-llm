import redis

cache = redis.Redis(host="redis", port=6379)

def get_cached_answer(query):

    return cache.get(query)

def set_cached_answer(query, answer):

    cache.set(query, answer, ex=3600)