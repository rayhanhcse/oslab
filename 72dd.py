# Deadlock Detection using Wait-For Graph (Cycle Detection)

from collections import defaultdict

class DeadlockDetection:
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
    processes = ["P1", "P2", "P3", "P4"]
    detector = DeadlockDetection(processes)

    # Example: P1 waits for P2, P2 waits for P3, P3 waits for P1 (cycle = deadlock)
    detector.add_edge("P1", "P2")
    detector.add_edge("P2", "P3")
    detector.add_edge("P3", "P1")

    if detector.detect_deadlock():
        print("Deadlock detected! (Cycle found in Wait-for Graph)")
    else:
        print("No deadlock detected.")
