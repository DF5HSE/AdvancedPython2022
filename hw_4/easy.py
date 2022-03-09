from time import time
from threading import Thread
from multiprocessing import Process


def fib(n):
    res = [1, 1]
    for i in range(2, n):
        res.append(res[i - 1] + res[i - 2])
    return res[-1]


if __name__ == "__main__":
    big_number = 100000
    file = open("artifacts/easy.txt", "w")

    start_time = time()
    for _ in range(10):
        fib(big_number)
    file.write(f"Synchronized launch time: {time() - start_time}s\n")

    threads = [Thread(target=fib, args=(big_number,)) for _ in range(10)]
    start_time = time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    file.write(f"10 threads time: {time() - start_time}s\n")

    processes = [Process(target=fib, args=(big_number, )) for _ in range(10)]
    start_time = time()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    file.write(f"10 processes time: {time() - start_time}s\n")

    file.close()


