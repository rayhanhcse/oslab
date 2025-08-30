# Banker's Algorithm (Deadlock Prevention)

def is_safe(processes, avail, max_need, alloc):
    n = len(processes)
    m = len(avail)

    need = [[max_need[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
    finish = [False] * n
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

if __name__ == "__main__":
    processes = [0, 1, 2, 3, 4]
    avail = [3, 3, 2]  # Available resources
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

    safe, seq = is_safe(processes, avail, max_need, alloc)
    if safe:
        print("System is in a safe state.")
        print("Safe sequence:", seq)
    else:
        print("System is NOT in a safe state (deadlock prevention needed).")
