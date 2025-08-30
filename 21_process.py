from multiprocessing import Process
import os

def child_process():
    print(f"Child Process: PID = {os.getpid()}, Parent PID = {os.getppid()}")
    print("Child terminating...")

if __name__ == "__main__":
    p = Process(target=child_process)
    print(f"Parent Process: PID = {os.getpid()}")
    p.start()   # Start child
    p.join()    # Wait for child to finish
    print("Parent terminating...")
