# -------------------------------
# Deadlock Avoidance: Banker's Algorithm
# -------------------------------

from typing import List, Tuple

class Bankers:
    def __init__(self, available: List[int], max_need: List[List[int]], alloc: List[List[int]]):
        self.available = available[:]                 # m
        self.max_need = [row[:] for row in max_need]  # n x m
        self.alloc = [row[:] for row in alloc]        # n x m
        self.n = len(self.alloc)
        self.m = len(self.available)

    def need(self) -> List[List[int]]:
        return [[self.max_need[i][j] - self.alloc[i][j] for j in range(self.m)]
                for i in range(self.n)]

    def is_safe(self) -> Tuple[bool, List[int]]:
        need = self.need()
        work = self.available[:]
        finish = [False] * self.n
        seq = []

        while len(seq) < self.n:
            progressed = False
            for i in range(self.n):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(self.m)):
                    # i can finish
                    for j in range(self.m):
                        work[j] += self.alloc[i][j]
                    finish[i] = True
                    seq.append(i)
                    progressed = True
            if not progressed:
                return False, []
        return True, seq

    def request(self, pid: int, req: List[int]) -> bool:
        """Try to grant a request. Returns True if granted, False otherwise."""
        need = self.need()
        # Rule 1: req <= need[pid]
        if any(req[j] > need[pid][j] for j in range(self.m)):
            print(f"[DENY] P{pid} requested more than its declared maximum.")
            return False
        # Rule 2: req <= available
        if any(req[j] > self.available[j] for j in range(self.m)):
            print(f"[WAIT] P{pid} must wait; not enough available resources.")
            return False

        # Tentatively allocate
        for j in range(self.m):
            self.available[j] -= req[j]
            self.alloc[pid][j] += req[j]

        safe, seq = self.is_safe()
        if safe:
            print(f"[GRANTED] Request by P{pid}: {req}. Safe sequence: {seq}")
            return True
        else:
            # Roll back
            for j in range(self.m):
                self.available[j] += req[j]
                self.alloc[pid][j] -= req[j]
            print(f"[DENY] Request by P{pid}: {req} would lead to UNSAFE state.")
            return False

if __name__ == "__main__":
    # Example from many OS texts
    available = [3, 3, 2]
    max_need = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    alloc = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    sys = Bankers(available, max_need, alloc)

    ok, seq = sys.is_safe()
    print("Initial safe state?", ok, "| Safe sequence:" if ok else "", seq if ok else "")
    # Try a few requests
    sys.request(1, [1, 0, 2])   # P1 asks for (1,0,2)
    sys.request(4, [3, 3, 0])   # P4 asks for (3,3,0)
    sys.request(0, [0, 2, 0])   # P0 asks for (0,2,0)
