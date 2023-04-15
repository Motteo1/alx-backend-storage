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