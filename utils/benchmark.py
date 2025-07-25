import functools
import time


def benchmark(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[BENCHMARK] {func.__name__} - {end - start:.4f} секунд")
        return result

    return wrapper
