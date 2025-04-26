from inspect import getfullargspec


def check_function_spec(func, kwargs: dict):
    spec = getfullargspec(func)
    if spec.varkw:
        return kwargs

    return {k: v for k, v in kwargs.items() if k in set(spec.args + spec.kwonlyargs)}
