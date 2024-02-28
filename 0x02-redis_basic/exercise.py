"""The following script contains the class definition for redis cache
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a function is called
        Args:
            method: The function to be decorated
        Returns:
            The decorated function
    """
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Args:
            self: The object instance
            *args: The arguments passed to the function
            **kwargs: The keyword arguments passed to the function
        Returns:
        The return value of the decorated function
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to record the history of function calls
    Args:
        method: The function to be decorated
    Returns:
        The decorated function
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Args:
            self: The object instance
            *args: The arguments passed to the function
            **kwargs: The keyword arguments passed to the function
        Returns:
            The return value of the decorated function
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data


    return wrapper


def replay(fn: Callable):
    """
    Replays the history of a function
    """
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0
    print("{} was called {} times:".format(function_name, value))
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)
    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input =""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""
        print("{}(*{}) -> {}".format(function_name, input, output))


class Cache:
    """
    this class defines methods to handle redis cache operations
    """
    def __init__(self) -> None:
    """
    Initialize redis client
    Attributtes:
        self._redis (redis.Redis): redis client
    """
    self._redis = redis.Redis()
    self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
    """
    Store data in redis cache
    """
    key = str(uuid.uuid4())
    self._redis.set(key, data)
    return key


    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ Get data from redis cache"""
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data


    def get_str(self, key: str) -> str:
        """ Get data as string from redis cache
        Args:
            key (str): key
        Returns:
            str: data
        """
        data = self_redis.get(key)
        return data.decode("utf-8")


    def get_int(self, key: str) -> int:
        """ Get data as integer from redis cache
        Args:
            key (str): key
        Returns:
            int: data
        """
        data = self_redis.get(key)
        try:
            data = int(data.decode("utf-8"0))
        except Exception:
            data: 0
        return data
