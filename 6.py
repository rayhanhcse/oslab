import threading
import time
import random

# Shared resource
data = 0
read_count = 0

# Semaphores
mutex = threading.Semaphore(1)   # Protects read_count
rw_mutex = threading.Semaphore(1)  # Controls access to resource

def reader(id):
    global read_count, data
    while True:
        mutex.acquire()
        read_count += 1
        if read_count == 1:
            rw_mutex.acquire()  # First reader locks writers
        mutex.release()

        # Reading section
        print(f"Reader {id} is reading data = {data}")
        time.sleep(random.uniform(0.5, 2))

        mutex.acquire()
        read_count -= 1
        if read_count == 0:
            rw_mutex.release()  # Last reader unlocks writers
        mutex.release()
        time.sleep(random.uniform(0.5, 2))

def writer(id):
    global data
    while True:
        rw_mutex.acquire()  # Lock resource for writing
        data += 1
        print(f"Writer {id} wrote data = {data}")
        rw_mutex.release()
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    readers = [threading.Thread(target=reader, args=(i,)) for i in range(3)]
    writers = [threading.Thread(target=writer, args=(i,)) for i in range(2)]

    for t in readers + writers:
        t.start()
    for t in readers + writers:
        t.join()
