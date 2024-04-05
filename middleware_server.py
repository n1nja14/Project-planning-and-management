import multiprocessing as mp
import time
import os


class Proc:
    def __init__(self, queue: mp.Queue):
        self.queue = queue
        self.run()

    def run(self):
        while 1:
            if self.queue.empty():
                query = self.queue.get()

            time.sleep(1)


class Server:
    QUEUE_CHECKING_INTERVAL = 1

    def __init__(self):
        self.query_queue = mp.Queue()
        self.process = mp.Process(
            target=Proc,
            args=(self.query_queue,),
            daemon=False
        )
        self.process.start()


if __name__ == "__main__":
    server = Server()


