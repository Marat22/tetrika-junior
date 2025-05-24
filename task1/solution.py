from typing import Callable
from functools import wraps
import inspect


def strict(func: Callable):
    sig = inspect.signature(func)
    annotations = func.__annotations__
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)

        for name, value in bound_args.arguments.items():
            if name in annotations and not isinstance(value, annotations[name]):
                raise TypeError
        
        return func(*args, **kwargs)
    
    return wrapper
