import multiprocessing as mp
import time

class Proc:
    def __init__(self, queue: mp.Queue):
        self.queue = queue

    def run(self, queue: mp.Queue):
        while 1:

            time.sleep(1)

class Server:
    QUEUE_CHECKING_INTERVAL = 1

    def __init__(self):
        self.query_queue = mp.Queue()
        self.process = mp.Process(
            target=Proc,
            args=(self.query_queue, )
        )
        


