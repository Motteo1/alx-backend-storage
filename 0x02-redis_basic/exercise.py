#!/usr/bin/env python3
""" The Redis Module """

from functools import wraps
import redis
import sys
from typing import Callable, Optional, Union
from uuid import uuid4


def replay(method: Callable):
    """Replay function"""
    key = method.__qualname__
    p = "".join([key, ":inputs"])
    q = "".join([key, ":outputs"])
    count = method.__self__get(key)
    p_list = method.__self__.lrange(p, 0, -1)
    q_list = method.__self__.lrange(q, 0, -1)
    queue = list(zip(p_list, q_list))
    print(f"{key} was called {decode_utf8(count)} times:")
    for k, v, in queue:
        k = decode_utf8(k)
        v = decode_utf8(v)
        print(f"{key}(*{k}) -> {v}")


def call_history(method: Callable) -> Callable:
    """ Call History """
    key = method.__qualname__
    p = "".join([key, ":inputs"])
    q = "".join([key, ":outputs"])
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self.redis.rpush(p, str(args))
        res = method(self, *args, **kwargs)
        self.redis.rpush(q, str(res))
        return res
    return wrapper


def count_calls(method: Callable) -> Callable:
    """ Count Calls """
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self.redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def decode_utf8(b: bytes) -> str:
    """ Decode utf8 """
    return b.decode('utf-8') if type(b) == bytes else b


class Cache:
    """ Cache Class """

    def __init__(self):
        """ Init Cache """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int. float]) -> str:
        """ Store random """
        key = str(uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str,
                                                                    bytes,
                                                                    int,
                                                                    float]:
        """ Get random """
        res = self._redis.get(key)
        return fn(res) if fn else res
    
    