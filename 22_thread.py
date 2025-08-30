import threading
import os

def thread_function():
    print(f"Thread started: Thread ID = {threading.get_ident()}, in Process = {os.getpid()}")
    print("Thread terminating...")

if __name__ == "__main__":
    print(f"Main Process: PID = {os.getpid()}")
    t = threading.Thread(target=thread_function)
    t.start()   # Start thread
    t.join()    # Wait for thread to finish
    print("Main process terminating...")
