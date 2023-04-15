#!/usr/bin/env python3
""" The Redis Module """

from functools import wraps
import redis
import sys
from typing import Callable, Optional, Union
from uuid import uuid4

def replay(method: Callable):