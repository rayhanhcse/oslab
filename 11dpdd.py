
from typing import List
from collections import defaultdict


def is_safe(processes: List[int], avail: List[int], max_need: List[List[int]], alloc: List[List[int]]):
    n, m = len(processes), len(avail)
    need = [[max_need[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
    finish = [False]*n
    safe_seq = []
    work = avail[:]

    while len(safe_seq) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += alloc[i][j]
                safe_seq.append(processes[i])
                finish[i] = True
                found = True
        if not found:
            return False, []
    return True, safe_seq

def request_resources(pid, req, processes, avail, max_need, alloc):
    need = [[max_need[i][j] - alloc[i][j] for j in range(len(avail))] for i in range(len(processes))]
    if any(req[j] > need[pid][j] for j in range(len(avail))):
        print(f"[DENY] Request exceeds maximum need for P{pid}.")
        return False
    if any(req[j] > avail[j] for j in range(len(avail))):
        print(f"[WAIT] Resources unavailable for P{pid}. Request must wait.")
        return False
    # Tentative allocation
    for j in range(len(avail)):
        avail[j] -= req[j]
        alloc[pid][j] += req[j]
    safe, seq = is_safe(processes, avail, max_need, alloc)
    if safe:
        print(f"[GRANT] Request granted for P{pid}. Safe sequence: {seq}")
        return True
    else:
        # Rollback
        for j in range(len(avail)):
            avail[j] += req[j]
            alloc[pid][j] -= req[j]
        print(f"[DENY] Request denied for P{pid}. Unsafe state!")
        return False


class DeadlockDetector:
    def __init__(self, processes):
        self.graph = defaultdict(list)
        self.processes = processes

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def is_cyclic_util(self, v, visited, rec_stack):
        visited[v] = True
        rec_stack[v] = True
        for neighbour in self.graph[v]:
            if not visited[neighbour]:
                if self.is_cyclic_util(neighbour, visited, rec_stack):
                    return True
            elif rec_stack[neighbour]:
                return True
        rec_stack[v] = False
        return False

    def detect_deadlock(self):
        visited = {p: False for p in self.processes}
        rec_stack = {p: False for p in self.processes}
        for node in self.processes:
            if not visited[node]:
                if self.is_cyclic_util(node, visited, rec_stack):
                    return True
        return False


if __name__ == "__main__":
    # Process and resource setup
    processes = [0,1,2,3,4]
    avail = [3,3,2]
    max_need = [
        [7,5,3],
        [3,2,2],
        [9,0,2],
        [2,2,2],
        [4,3,3]
    ]
    alloc = [
        [0,1,0],
        [2,0,0],
        [3,0,2],
        [2,1,1],
        [0,0,2]
    ]

    print("=== DEADLOCK PREVENTION (Banker's Algorithm) ===")
    safe, seq = is_safe(processes, avail, max_need, alloc)
    print("Initial safe state?", safe, "| Safe sequence:", seq if safe else [])

    # Sample resource requests
    request_resources(1, [1,0,2], processes, avail, max_need, alloc)
    request_resources(4, [3,3,0], processes, avail, max_need, alloc)

    print("\n=== DEADLOCK DETECTION (Wait-for Graph) ===")
    # Example: cycle P1->P2->P3->P1
    detector = DeadlockDetector(["P1","P2","P3","P4"])
    detector.add_edge("P1","P2")
    detector.add_edge("P2","P3")
    detector.add_edge("P3","P1")  # cycle
    detector.add_edge("P4","P2")  # optional extra edge

    if detector.detect_deadlock():
        print("Deadlock detected! (Cycle exists)")
    else:
        print("No deadlock detected.")
