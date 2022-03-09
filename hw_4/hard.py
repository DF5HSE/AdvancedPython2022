import codecs
from datetime import datetime
import sys
import time
from multiprocessing import Queue, Pipe, Process
from multiprocessing.connection import Connection


def a(main_to_a: Queue, a_to_b: Pipe):
    while True:
        while not main_to_a.empty():
            a_to_b.send(main_to_a.get_nowait().lower())
            time.sleep(5)


def b(a_to_b: Connection, b_to_main: Connection):
    while True:
        b_to_main.send(codecs.encode(a_to_b.recv(), "rot_13"))


if __name__ == '__main__':
    from_main_to_a = Queue()
    to_b_from_a, from_a_to_b = Pipe()
    to_main_from_b, from_b_to_main = Pipe()
    Process(target=a, args=(from_main_to_a, from_a_to_b), daemon=True).start()
    Process(target=b, args=(to_b_from_a, from_b_to_main), daemon=True).start()
    while True:
        from_main_to_a.put(input(f"[{datetime.now()}] input: "))
        res = to_main_from_b.recv()
        print(f"[{datetime.now()}] output: {res}")
