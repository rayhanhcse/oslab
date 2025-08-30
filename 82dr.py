# ---------------------------------------
# Deadlock Detection + Recovery Simulator
# ---------------------------------------

from typing import List, Dict, Set
from collections import defaultdict

def build_wait_for_graph(available: List[int], alloc: List[List[int]], request: List[List[int]]) -> Dict[int, Set[int]]:
    """
    Build a wait-for graph W:
    Add edge i -> j if process i is waiting for a resource type k such that:
      request[i][k] > available[k]  and  alloc[j][k] > 0
    This approximates who i is effectively waiting on.
    """
    n, m = len(alloc), len(available)
    W = defaultdict(set)

    # Which resource types are currently scarce?
    scarce = [available[k] == 0 for k in range(m)]

    for i in range(n):
        # Process i is waiting if any requested resource type k is not currently satisfiable
        waiting_types = [k for k in range(m) if request[i][k] > 0 and request[i][k] > available[k]]
        if not waiting_types:
            continue
        holders = set()
        for k in waiting_types:
            # processes j that hold resource k
            for j in range(n):
                if alloc[j][k] > 0 and j != i:
                    holders.add(j)
        for j in holders:
            W[i].add(j)
    return W

def find_cycle(W: Dict[int, Set[int]], n: int) -> List[int]:
    """Return one cycle as a list of nodes, or [] if no cycle."""
    visited = [0]*n  # 0=unseen,1=visiting,2=done
    parent = [-1]*n
    cycle = []

    def dfs(u: int) -> bool:
        nonlocal cycle
        visited[u] = 1
        for v in W.get(u, []):
            if visited[v] == 0:
                parent[v] = u
                if dfs(v):
                    return True
            elif visited[v] == 1:
                # found a back edge, reconstruct cycle u -> ... -> v -> u
                cyc = [u]
                x = u
                while x != v:
                    x = parent[x]
                    cyc.append(x)
                cyc.reverse()
                cycle = cyc
                return True
        visited[u] = 2
        return False

    for s in range(n):
        if visited[s] == 0 and dfs(s):
            return cycle
    return []

def choose_victim(cycle: List[int], alloc: List[List[int]]) -> int:
    """Select victim with **fewest total resources held** (min cost to abort/rollback)."""
    def held(i): return sum(alloc[i])
    return min(cycle, key=held)

def detect_and_recover(available: List[int], alloc: List[List[int]], request: List[List[int]]) -> None:
    """
    Repeatedly detect cycles; if any, choose a victim, abort it (release its allocation),
    and continue until no cycles remain.
    """
    step = 1
    while True:
        W = build_wait_for_graph(available, alloc, request)
        cycle = find_cycle(W, len(alloc))
        if not cycle:
            print("[OK] No deadlock. System can proceed.")
            break
        print(f"[DETECT] Deadlock cycle found among processes: {cycle}")
        v = choose_victim(cycle, alloc)
        print(f"[RECOVER] Aborting victim P{v} (releases {alloc[v]}).")
        # Release its resources
        for k in range(len(available)):
            available[k] += alloc[v][k]
            alloc[v][k] = 0
            request[v][k] = 0
        print(f"[STATE] After recovery step {step} -> Available = {available}")
        step += 1

if __name__ == "__main__":
    # Example snapshot with a deadlock
    # 3 resource types, 4 processes
    available = [0, 0, 0]
    alloc = [
        [1, 0, 1],  # P0 holds R0, R2
        [0, 1, 0],  # P1 holds R1
        [0, 0, 1],  # P2 holds R2
        [1, 0, 0],  # P3 holds R0
    ]
    # Requests that cannot be satisfied right now
    request = [
        [0, 1, 0],  # P0 needs R1
        [1, 0, 1],  # P1 needs R0, R2
        [1, 1, 0],  # P2 needs R0, R1
        [0, 0, 1],  # P3 needs R2
    ]

    print("Initial Available:", available)
    print("Initial Allocation:", alloc)
    print("Initial Request:", request)
    detect_and_recover(available, alloc, request)
