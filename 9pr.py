# -------------------------------
# Page Replacement Algorithms
# FIFO, LRU, LFU
# -------------------------------

from collections import deque, defaultdict

# FIFO Page Replacement
def fifo(pages, capacity):
    print("\n--- FIFO Page Replacement ---")
    frame = deque()
    page_faults = 0

    for page in pages:
        if page not in frame:
            page_faults += 1
            if len(frame) == capacity:
                removed = frame.popleft()
                print(f"Page {removed} removed")
            frame.append(page)
            print(f"Page {page} added -> Frame: {list(frame)}")
        else:
            print(f"Page {page} hit -> Frame: {list(frame)}")

    print(f"Total Page Faults (FIFO): {page_faults}\n")


# LRU Page Replacement
def lru(pages, capacity):
    print("\n--- LRU Page Replacement ---")
    frame = []
    page_faults = 0

    for i, page in enumerate(pages):
        if page not in frame:
            page_faults += 1
            if len(frame) == capacity:
                # Remove least recently used
                lru_page = min(frame, key=lambda p: pages[:i][::-1].index(p))
                frame.remove(lru_page)
                print(f"Page {lru_page} removed")
            frame.append(page)
            print(f"Page {page} added -> Frame: {frame}")
        else:
            print(f"Page {page} hit -> Frame: {frame}")

    print(f"Total Page Faults (LRU): {page_faults}\n")


# LFU Page Replacement
def lfu(pages, capacity):
    print("\n--- LFU Page Replacement ---")
    frame = []
    freq = defaultdict(int)
    page_faults = 0

    for i, page in enumerate(pages):
        freq[page] += 1
        if page not in frame:
            page_faults += 1
            if len(frame) == capacity:
                # Find LFU (if tie → earliest inserted)
                lfu_page = min(frame, key=lambda p: (freq[p], pages[:i].index(p)))
                frame.remove(lfu_page)
                print(f"Page {lfu_page} removed")
            frame.append(page)
            print(f"Page {page} added -> Frame: {frame}")
        else:
            print(f"Page {page} hit -> Frame: {frame}")

    print(f"Total Page Faults (LFU): {page_faults}\n")


# -------------------------------
# Driver Code
# -------------------------------
if __name__ == "__main__":
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]  # Reference string
    capacity = 3  # Number of frames

    fifo(pages, capacity)
    lru(pages, capacity)
    lfu(pages, capacity)
