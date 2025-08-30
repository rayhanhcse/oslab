def srtf(processes, burst_time, arrival_time):
    n = len(processes)
    remaining_time = burst_time.copy()
    waiting_time = [0] * n
    turnaround_time = [0] * n

    complete = 0
    t = 0
    minm = float('inf')
    shortest = 0
    check = False

    while complete != n:
        # Find process with minimum remaining time at current time t
        for j in range(n):
            if arrival_time[j] <= t and remaining_time[j] < minm and remaining_time[j] > 0:
                minm = remaining_time[j]
                shortest = j
                check = True

        if not check:
            t += 1
            continue

        # Reduce remaining time
        remaining_time[shortest] -= 1
        minm = remaining_time[shortest]
        if minm == 0:
            minm = float('inf')

        # If a process gets completely executed
        if remaining_time[shortest] == 0:
            complete += 1
            check = False
            finish_time = t + 1
            waiting_time[shortest] = (finish_time - burst_time[shortest] - arrival_time[shortest])
            if waiting_time[shortest] < 0:
                waiting_time[shortest] = 0

        t += 1

    # Calculate turnaround time
    for i in range(n):
        turnaround_time[i] = burst_time[i] + waiting_time[i]

    avg_wt = sum(waiting_time) / n
    avg_tat = sum(turnaround_time) / n

    print("\n=== Shortest Remaining Time First (SRTF) ===")
    print("Process\tArrival\tBurst\tWaiting\tTurnaround")
    for i in range(n):
        print(f"P{processes[i]}\t{arrival_time[i]}\t{burst_time[i]}\t{waiting_time[i]}\t{turnaround_time[i]}")
    print(f"Average Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")


def priority_scheduling(processes, burst_time, priority):
    n = len(processes)

    # Sort by priority
    sorted_data = sorted(zip(processes, burst_time, priority), key=lambda x: x[2])
    processes, burst_time, priority = zip(*sorted_data)

    waiting_time = [0] * n
    turnaround_time = [0] * n

    # Waiting time
    for i in range(1, n):
        waiting_time[i] = waiting_time[i-1] + burst_time[i-1]

    # Turnaround time
    for i in range(n):
        turnaround_time[i] = waiting_time[i] + burst_time[i]

    avg_wt = sum(waiting_time) / n
    avg_tat = sum(turnaround_time) / n

    print("\n=== Priority Scheduling (Non-Preemptive) ===")
    print("Process\tPriority\tBurst\tWaiting\tTurnaround")
    for i in range(n):
        print(f"P{processes[i]}\t{priority[i]}\t\t{burst_time[i]}\t{waiting_time[i]}\t{turnaround_time[i]}")
    print(f"Average Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")


if __name__ == "__main__":
    n = int(input("Enter number of processes: "))

    processes = []
    burst_time = []
    arrival_time = []
    priority = []

    for i in range(n):
        processes.append(i+1)
        at = int(input(f"Enter Arrival Time for Process P{i+1}: "))
        bt = int(input(f"Enter Burst Time for Process P{i+1}: "))
        pr = int(input(f"Enter Priority (lower = higher priority) for Process P{i+1}: "))
        arrival_time.append(at)
        burst_time.append(bt)
        priority.append(pr)

    # Run both algorithms
    srtf(processes, burst_time, arrival_time)
    priority_scheduling(processes, burst_time, priority)
