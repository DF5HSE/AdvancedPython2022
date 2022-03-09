import math
import os
from datetime import datetime
from time import time
from concurrent.futures import ProcessPoolExecutor


def _integrate_synchronized(args):
    f, a, b, step = args
    print(
        f"[{datetime.now()}, process {os.getpid()}] Start process with integrate function {f.__name__} from {a} to {b}"
        f" by step {step}"
    )
    range_ends = [a + step]
    while range_ends[-1] + step < b:
        range_ends.append(range_ends[-1] + step)
    acc = sum(f(range_end) for range_end in range_ends) * step
    print(
        f"[{datetime.now()}, process {os.getpid()}] End process integrate function {f.__name__} from {a} to {b} by step {step}"
    )
    return acc


def integrate(f, a, b, *, n_jobs=1, n_iter=1000):
    print(
        f"[{datetime.now()}] Start integrate function {f.__name__} from {a} to {b} with n_jobs={n_jobs} and n_iter={n_iter}"
    )
    jobs_step = (b - a) / n_jobs
    iter_step = (b - a) / n_iter

    pool = ProcessPoolExecutor(max_workers=n_jobs)
    starts = [a]
    while starts[-1] + jobs_step < b:
        starts.append(starts[-1] + jobs_step)
    acc = sum(pool.map(
        _integrate_synchronized,
        [(f, start, start + jobs_step, iter_step) for start in starts]
    ))
    print(
        f"[{datetime.now()}] End integrate function {f.__name__} from {a} to {b} with n_jobs={n_jobs} and n_iter={n_iter}"
    )
    return acc


if __name__ == "__main__":
    time_compare_file = open("artifacts/medium_time_compare.txt", "w")

    for n in range(1, os.cpu_count() * 2 + 1):
        start_time = time()
        integrate(math.cos, 0, math.pi / 2, n_jobs=n, n_iter=1000000)
        time_compare_file.write(f"Time with n_jobs={n}: {time() - start_time}s\n")

    time_compare_file.close()
